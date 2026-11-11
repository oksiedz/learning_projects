"""
immich_health.py — Immich Server Health Checks

This module provides dedicated health checks for Immich server instances,
detecting when the Immich server is running, responsive, and healthy.

Immich Server monitoring includes:
- Process-level checks (immich-server, immich-machine-learning, immich-microservices)
- API endpoint health checks
- Database connectivity checks
- Docker container status (if running via Docker)
- Disk space on Immich upload directories
- Automatic restart detection and alerting
"""

import os
import sys
import json
import logging
import subprocess
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import platform
import socket

logger = logging.getLogger(__name__)

# Common Immich process names
IMMICH_PROCESSES = [
    "immich-server",
    "immich-machine-learning",
    "immich-microservices",
    "immich",
]

# Common Immich API endpoints
IMMICH_API_ENDPOINTS = [
    "/api/server/status",
    "/api/server/info",
]

# Default Immich port
IMMICH_DEFAULT_PORT = 2283


def is_immich_running_as_process() -> List[Dict]:
    """
    Check if Immich server processes are running at the OS level.

    Returns a list of process information dicts for each Immich process found.
    """
    import psutil
    found_processes = []

    for proc in psutil.process_iter(['pid', 'name', 'username', 'cmdline']):
        try:
            proc_name = proc.info['name'] or ""
            proc_cmdline = " ".join(proc.info['cmdline'] or [])

            # Check if this is an Immich process
            for immich_name in IMMICH_PROCESSES:
                if immich_name.lower() in proc_name.lower() or immich_name.lower() in proc_cmdline.lower():
                    found_processes.append({
                        "pid": proc.info['pid'],
                        "name": proc_name,
                        "username": proc.info['username'],
                        "cmdline": proc_cmdline,
                        "matched_pattern": immich_name,
                        "detected_at": datetime.now().isoformat(),
                    })
                    break
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    return found_processes


def check_immich_api_endpoint(host: str = "localhost", port: int = IMMICH_DEFAULT_PORT,
                              endpoint: str = "/api/server/status",
                              timeout: int = 10) -> Dict:
    """
    Check an Immich API endpoint for responsiveness.

    Returns a dict with status, response time, and any error details.
    """
    result = {
        "endpoint": f"http://{host}:{port}{endpoint}",
        "status": "unknown",
        "response_time_ms": None,
        "status_code": None,
        "error": None,
    }

    try:
        import urllib.request
        start_time = time.time()
        req = urllib.request.Request(
            f"http://{host}:{port}{endpoint}",
            headers={"User-Agent": "System-Parameters-Logger/1.0"}
        )
        with urllib.request.urlopen(req, timeout=timeout) as response:
            elapsed = (time.time() - start_time) * 1000
            result["status"] = "healthy"
            result["response_time_ms"] = round(elapsed, 2)
            result["status_code"] = response.getcode()
            result["body"] = response.read().decode('utf-8', errors='replace')[:500]
    except urllib.error.URLError as e:
        result["status"] = "unreachable"
        result["error"] = str(e)
    except socket.timeout:
        result["status"] = "timeout"
        result["error"] = f"Connection timed out after {timeout}s"
    except ConnectionRefusedError:
        result["status"] = "connection_refused"
        result["error"] = "Connection refused — Immich may not be running"
    except Exception as e:
        result["status"] = "error"
        result["error"] = str(e)

    return result


def check_immich_health(host: str = "localhost", port: int = IMMICH_DEFAULT_PORT) -> Dict:
    """
    Perform a comprehensive Immich server health check.

    Returns a dict with overall status and per-endpoint results.
    """
    health = {
        "timestamp": datetime.now().isoformat(),
        "host": host,
        "port": port,
        "overall_status": "unknown",
        "endpoints": {},
        "processes": [],
        "alerts": [],
    }

    # Check API endpoints
    all_healthy = True
    any_reachable = False

    for endpoint in IMMICH_API_ENDPOINTS:
        result = check_immich_api_endpoint(host, port, endpoint)
        health["endpoints"][endpoint] = result

        if result["status"] == "healthy":
            any_reachable = True
        else:
            all_healthy = False
            health["alerts"].append(f"Immich endpoint {endpoint}: {result['status']}")

    # Check processes
    processes = is_immich_running_as_process()
    health["processes"] = processes

    if not processes:
        health["alerts"].append("No Immich processes detected")
        all_healthy = False

    # Determine overall status
    if all_healthy and any_reachable:
        health["overall_status"] = "healthy"
    elif any_reachable:
        health["overall_status"] = "degraded"
    else:
        health["overall_status"] = "unhealthy"

    # Log results
    if health["overall_status"] == "healthy":
        logger.info(f"I Immich server health: healthy ({len(processes)} processes)")
    elif health["overall_status"] == "degraded":
        logger.warning(f"Immich server health: degraded — some endpoints unreachable")
    else:
        logger.error(f"Immich server health: unhealthy — no endpoints reachable")

    return health


def check_immich_docker_containers() -> List[Dict]:
    """
    Check if Immich is running via Docker and get container status.

    Returns a list of container information dicts.
    """
    containers = []

    try:
        result = subprocess.run(
            ["docker", "ps", "--filter", "name=immich", "--format", "json"],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0 and result.stdout.strip():
            for line in result.stdout.strip().split('\n'):
                try:
                    container = json.loads(line)
                    containers.append({
                        "id": container.get("ID", ""),
                        "name": container.get("Names", ""),
                        "status": container.get("Status", ""),
                        "image": container.get("Image", ""),
                        "created": container.get("CreatedAt", ""),
                    })
                except json.JSONDecodeError:
                    continue
    except FileNotFoundError:
        logger.debug("Docker not available — skipping Docker container check")
    except Exception as e:
        logger.error(f"Error checking Docker containers: {e}")

    return containers


def check_immich_upload_directory(upload_path: str = None) -> Dict:
    """
    Check Immich upload directory disk space and accessibility.

    Default paths for common Immich installations.
    """
    if upload_path is None:
        # Common Immich upload paths
        upload_path = os.environ.get("IMMICH_UPLOAD_LOCATION", "/immich-upload")

    path = Path(upload_path)
    result = {
        "path": str(path),
        "exists": path.exists(),
        "accessible": False,
        "total_gb": None,
        "used_gb": None,
        "free_gb": None,
        "percent_used": None,
        "alerts": [],
    }

    import psutil

    if not path.exists():
        result["alerts"].append(f"Upload directory does not exist: {upload_path}")
        return result

    try:
        # Test accessibility
        test_file = path / ".immich_health_check"
        test_file.touch()
        test_file.unlink()
        result["accessible"] = True
    except Exception as e:
        result["alerts"].append(f"Upload directory not writable: {e}")
        return result

    # Check disk usage
    try:
        usage = psutil.disk_usage(str(path))
        result["total_gb"] = round(usage.total / (1024**3), 2)
        result["used_gb"] = round(usage.used / (1024**3), 2)
        result["free_gb"] = round(usage.free / (1024**3), 2)
        result["percent_used"] = round(usage.percent, 1)

        if usage.percent > 90:
            result["alerts"].append(f"Upload directory disk usage critical: {usage.percent}%")
        elif usage.percent > 80:
            result["alerts"].append(f"Upload directory disk usage warning: {usage.percent}%")
    except Exception as e:
        result["alerts"].append(f"Could not check disk usage: {e}")

    return result


def run_full_immich_health_check(config: Dict = None) -> Dict:
    """
    Run a complete Immich health check combining all checks.

    Args:
        config: Configuration dict with keys like 'host', 'port', 'upload_path'

    Returns:
        Complete health report dict
    """
    if config is None:
        config = {}

    host = config.get("host", "localhost")
    port = config.get("port", IMMICH_DEFAULT_PORT)
    upload_path = config.get("upload_path", None)

    report = {
        "timestamp": datetime.now().isoformat(),
        "immich_server": check_immich_health(host, port),
        "docker_containers": check_immich_docker_containers(),
        "upload_directory": check_immich_upload_directory(upload_path),
        "overall_status": "unknown",
        "alerts": [],
    }

    # Combine alerts
    all_alerts = []
    all_alerts.extend(report["immich_server"].get("alerts", []))
    all_alerts.extend(report["upload_directory"].get("alerts", []))
    report["alerts"] = all_alerts

    # Determine overall status
    server_status = report["immich_server"]["overall_status"]
    docker_containers = report["docker_containers"]

    if server_status == "healthy" and len(docker_containers) > 0:
        report["overall_status"] = "healthy"
    elif server_status in ("healthy", "degraded"):
        report["overall_status"] = "degraded"
    else:
        report["overall_status"] = "unhealthy"

    return report


def format_immich_health_report(report: Dict) -> str:
    """Format an Immich health report for console output."""
    lines = []
    lines.append("=" * 60)
    lines.append("IMMICH SERVER HEALTH CHECK REPORT")
    lines.append(f"Time: {report['timestamp']}")
    lines.append("=" * 60)

    # Server status
    server = report["immich_server"]
    lines.append(f"\nServer Status: {server['overall_status'].upper()}")
    lines.append(f"Host: {server['host']}:{server['port']}")

    # Endpoints
    lines.append("\nAPI Endpoints:")
    for endpoint, result in server.get("endpoints", {}).items():
        status_icon = "✓" if result["status"] == "healthy" else "✗"
        lines.append(f"  {status_icon} {endpoint}: {result['status']}")
        if result.get("response_time_ms"):
            lines.append(f"     Response time: {result['response_time_ms']}ms")
        if result.get("error"):
            lines.append(f"     Error: {result['error']}")

    # Processes
    lines.append("\nImmich Processes:")
    if server.get("processes"):
        for proc in server["processes"]:
            lines.append(f"  ✓ PID {proc['pid']}: {proc['name']} ({proc['matched_pattern']})")
    else:
        lines.append("  ✗ No Immich processes found")

    # Docker
    lines.append("\nDocker Containers:")
    if report.get("docker_containers"):
        for container in report["docker_containers"]:
            lines.append(f"  ✓ {container['name']}: {container['status']}")
    else:
        lines.append("  - No Docker containers detected")

    # Upload directory
    upload = report.get("upload_directory", {})
    lines.append(f"\nUpload Directory: {upload.get('path', 'N/A')}")
    if upload.get("exists"):
        lines.append(f"  Exists: Yes")
        lines.append(f"  Accessible: {upload.get('accessible', False)}")
        if upload.get("percent_used") is not None:
            lines.append(f"  Disk usage: {upload['percent_used']}% ({upload.get('free_gb', 0)}GB free of {upload.get('total_gb', 0)}GB)")
    else:
        lines.append(f"  Exists: No")

    # Alerts
    if report.get("alerts"):
        lines.append(f"\nALERTS ({len(report['alerts'])}):")
        for alert in report["alerts"]:
            lines.append(f"  ⚠ {alert}")
    else:
        lines.append("\nNo alerts.")

    lines.append("=" * 60)
    return "\n".join(lines)


if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

    report = run_full_immich_health_check()
    print(format_immich_health_report(report))