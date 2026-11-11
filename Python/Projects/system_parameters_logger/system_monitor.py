"""
System Parameters Logger - Main Monitoring Script

This is the core monitoring module that continuously tracks system parameters
including CPU usage, memory consumption, disk status, network connectivity,
and system processes. It's designed to help diagnose issues when remote access
becomes problematic.

Key Features:
- Continuous system monitoring with configurable intervals
- Network health monitoring with ping tests
- Process and application monitoring
- Configurable alert thresholds
- Detailed logging with rotation support
- Cross-platform compatibility

Usage:
    python system_monitor.py [--interval INTERVAL] [--config CONFIG_FILE]
"""

import os
import sys
import time
import json
import logging
import subprocess
import threading
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import platform
import socket
import psutil

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Local imports
from config import (
    LOG_DIR,
    CONFIG_DIR,
    config,
    save_config,
    load_config,
    LOGGING_CONFIG,
    CPU_THRESHOLD,
    MEMORY_THRESHOLD,
    DISK_THRESHOLD,
    PING_THRESHOLD,
    CPU_CHECK_INTERVAL,
    MEMORY_CHECK_INTERVAL,
    DISK_CHECK_INTERVAL,
    NETWORK_CHECK_INTERVAL,
    PROCESS_CHECK_INTERVAL,
    MONITORED_APPLICATIONS
)

# Logging setup
LOG_FILE = LOG_DIR / "system_monitor.log"

# Create log directory if it doesn't exist
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Configure logging
logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

# Global state for monitoring
monitoring_state = {
    "monitoring_active": False,
    "start_time": None,
    "last_check_times": {},
    "alert_cooldowns": {},
}

# Initialize application monitoring state
app_monitoring_state = {}

def setup_logging():
    """Setup logging with file rotation and console output."""
    # Create log directory
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    # Remove existing handlers to avoid duplicates
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    # Create formatters
    detailed_formatter = logging.Formatter(
        fmt=config["logging"]["format"],
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    simple_formatter = logging.Formatter(
        fmt="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%H:%M:%S"
    )

    # File handler with rotation
    file_handler = logging.handlers.RotatingFileHandler(
        filename=LOG_FILE,
        maxBytes=config["logging"]["max_log_size_mb"] * 1024 * 1024,
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(config["logging"]["level"])
    file_handler.setFormatter(detailed_formatter)
    logging.root.addHandler(file_handler)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(config["logging"]["level"] if config["logging"]["console_output"] else "WARNING")
    console_handler.setFormatter(simple_formatter if config["logging"]["level"] == "DEBUG" else detailed_formatter)
    logging.root.addHandler(console_handler)

    # Root logger
    logging.root.setLevel(config["logging"]["level"])

def cleanup_old_logs():
    """Clean up old log files and alerts."""
    try:
        # Clean up logs older than retention period
        cutoff_date = datetime.now() - timedelta(days=config["monitoring"]["log_retention_days"])
        cutoff_timestamp = cutoff_date.timestamp()

        # Clean up log files
        log_files = list(LOG_DIR.glob("*.log"))
        for log_file in log_files:
            try:
                if log_file.stat().st_mtime < cutoff_timestamp:
                    log_file.unlink()
                    logger.info(f"Removed old log file: {log_file}")
            except Exception as e:
                logger.warning(f"Could not remove {log_file}: {e}")

        # Clean up metrics files
        metrics_files = list(LOG_DIR.glob("system_metrics_*.json"))
        for metrics_file in metrics_files:
            try:
                if metrics_file.stat().st_mtime < cutoff_timestamp:
                    metrics_file.unlink()
                    logger.info(f"Removed old metrics file: {metrics_file}")
            except Exception as e:
                logger.warning(f"Could not remove {metrics_file}: {e}")

        # Clean up summary file if it's old
        summary_file = LOG_DIR / "monitoring_summary.txt"
        if summary_file.exists():
            if summary_file.stat().st_mtime < cutoff_timestamp:
                summary_file.unlink()
                logger.info(f"Removed old summary file: {summary_file}")

    except Exception as e:
        logger.error(f"Error during cleanup: {e}")

def check_cpu_usage() -> float:
    """Check CPU usage percentage."""
    try:
        return psutil.cpu_percent(interval=1)
    except Exception as e:
        logger.error(f"Error checking CPU usage: {e}")
        return -1

def check_memory_usage() -> Dict:
    """Check memory usage details."""
    try:
        memory = psutil.virtual_memory()
        return {
            "total": memory.total,
            "available": memory.available,
            "percent": memory.percent,
            "used": memory.used,
            "free": memory.free,
            "active": memory.active,
            "inactive": memory.inactive,
        }
    except Exception as e:
        logger.error(f"Error checking memory usage: {e}")
        return {}

def check_disk_usage() -> Dict:
    """Check disk usage for all partitions."""
    try:
        disk_info = {}
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disk_info[partition.mountpoint] = {
                    "device": partition.device,
                    "fstype": partition.fstype,
                    "total": usage.total,
                    "used": usage.used,
                    "free": usage.free,
                    "percent": usage.percent
                }
            except PermissionError:
                logger.warning(f"Permission denied accessing partition: {partition.mountpoint}")
            except Exception as e:
                logger.warning(f"Error checking disk usage for {partition.mountpoint}: {e}")

        return disk_info
    except Exception as e:
        logger.error(f"Error checking disk usage: {e}")
        return {}

def check_network_connectivity() -> Dict:
    """Check network connectivity by pinging multiple targets."""
    try:
        network_info = {
            "timestamp": datetime.now().isoformat(),
            "targets": {},
            "overall_status": "unknown"
        }

        ping_targets = config["network"]["ping_targets"]
        timeout = config["network"]["connection_timeout"]

        for target in ping_targets:
            try:
                # Use subprocess to run ping command
                if platform.system() == "Windows":
                    ping_cmd = ["ping", "-n", "4", "-w", str(timeout * 1000), target]
                else:
                    ping_cmd = ["ping", "-c", "4", "-W", str(timeout), target]

                result = subprocess.run(
                    ping_cmd,
                    capture_output=True,
                    text=True,
                    timeout=timeout + 5
                )

                if result.returncode == 0:
                    # Parse ping output to get average time
                    avg_time = None
                    if "average" in result.stdout or "avg" in result.stdout:
                        for line in result.stdout.split('\n'):
                            if "average" in line or "avg" in line:
                                try:
                                    # Extract the time from average line
                                    parts = line.split('/')
                                    if len(parts) >= 4:
                                        avg_time = float(parts[3])
                                except (ValueError, IndexError):
                                    pass

                    network_info["targets"][target] = {
                        "status": "reachable",
                        "avg_time_ms": avg_time,
                        "raw_output": result.stdout
                    }
                else:
                    network_info["targets"][target] = {
                        "status": "unreachable",
                        "error": result.stderr.strip() or f"Exit code: {result.returncode}",
                        "raw_output": result.stdout
                    }

            except subprocess.TimeoutExpired:
                network_info["targets"][target] = {
                    "status": "timeout",
                    "error": "Ping timed out"
                }
            except FileNotFoundError:
                network_info["targets"][target] = {
                    "status": "error",
                    "error": "ping command not found"
                }
            except Exception as e:
                network_info["targets"][target] = {
                    "status": "error",
                    "error": str(e)
                }

        # Determine overall status
        reachable_count = sum(1 for target in network_info["targets"].values() if target["status"] == "reachable")
        total_count = len(network_info["targets"])

        if reachable_count == total_count:
            network_info["overall_status"] = "healthy"
            logger.info("Network status: All targets reachable")
        elif reachable_count > 0:
            network_info["overall_status"] = "partial"
            logger.warning(f"Network status: Partial connectivity ({reachable_count}/{total_count} targets)")
        else:
            network_info["overall_status"] = "unreachable"
            logger.error("Network status: All targets unreachable")

        return network_info

    except Exception as e:
        logger.error(f"Error checking network connectivity: {e}")
        return {"overall_status": "error", "error": str(e)}

def check_processes() -> Dict:
    """Check status of monitored processes and applications."""
    try:
        process_info = {
            "timestamp": datetime.now().isoformat(),
            "monitored_processes": {},
            "critical_processes_down": []
        }

        # Check monitored applications
        for app_config in MONITORED_APPLICATIONS:
            try:
                app_name = app_config["name"]
                process_name = app_config["process_name"].lower()

                # Try to find the process by name
                processes_found = False
                for proc in psutil.process_iter(['pid', 'name', 'username']):
                    try:
                        if process_name in proc.info['name'].lower():
                            processes_found = True
                            process_info["monitored_processes"][app_name] = {
                                "status": "running",
                                "pid": proc.info['pid'],
                                "username": proc.info['username']
                            }
                            break
                    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                        continue

                if not processes_found:
                    process_info["monitored_processes"][app_name] = {
                        "status": "not_found",
                        "error": f"Process '{process_name}' not found"
                    }
                    if app_config.get("critical", False):
                        process_info["critical_processes_down"].append(app_name)
                        logger.error(f"CRITICAL: Application '{app_name}' process not found!")

            except Exception as e:
                logger.error(f"Error checking application '{app_config.get('name', 'unknown')}': {e}")

        # Check system processes
        system_processes = {}
        try:
            for proc in psutil.process_iter(['pid', 'name', 'username']):
                try:
                    system_processes[proc.info['name']] = system_processes.get(proc.info['name'], 0) + 1
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
        except Exception as e:
            logger.error(f"Error iterating system processes: {e}")

        process_info["system_processes"] = system_processes

        return process_info

    except Exception as e:
        logger.error(f"Error checking processes: {e}")
        return {"error": str(e)}

def write_metrics_to_summary(metrics: Dict):
    """Write metrics to summary file."""
    try:
        summary_file = LOG_DIR / "monitoring_summary.txt"

        # Create summary if it doesn't exist
        if not summary_file.exists():
            summary_content = (
                "="*80 + "\n"
                "SYSTEM MONITORING SUMMARY\n"
                f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                "="*80 + "\n"
            )
            with open(summary_file, 'w') as f:
                f.write(summary_content)

        # Append current metrics
        with open(summary_file, 'a') as f:
            f.write("\n")
            f.write(f"--- Check at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---\n")

            # System info
            if "system" in metrics:
                system_info = metrics["system"]
                f.write(f"Hostname: {system_info.get('hostname', 'N/A')}\n")
                f.write(f"Platform: {system_info.get('platform', 'N/A')} {system_info.get('platform_version', '')}\n")
                f.write(f"Uptime: {system_info.get('uptime', 'N/A')}\n")
                f.write("\n")

            # CPU
            if "cpu" in metrics:
                f.write(f"CPU Usage: {metrics['cpu']['percent']}%\n")
                f.write("\n")

            # Memory
            if "memory" in metrics:
                memory = metrics["memory"]
                f.write(f"Memory Usage: {memory['percent']}%\n")
                f.write(f"  Used: {memory['used']/(1024**3):.2f} GB\n")
                f.write(f"  Available: {memory['available']/(1024**3):.2f} GB\n")
                f.write(f"  Total: {memory['total']/(1024**3):.2f} GB\n")
                f.write("\n")

            # Disk
            if "disk" in metrics:
                f.write("Disk Usage:\n")
                for mountpoint, disk_info in metrics['disk'].items():
                    f.write(f"  {mountpoint}: {disk_info['percent']}% ({disk_info['used']/(1024**3):.2f}GB / {disk_info['total']/(1024**3):.2f}GB)\n")
                f.write("\n")

            # Network
            if "network" in metrics:
                network = metrics["network"]
                f.write(f"Network Status: {network.get('overall_status', 'unknown')}\n")
                f.write(f"  Targets: {len(network.get('targets', {}))}\n")
                if network.get('overall_status') == 'healthy':
                    f.write("  All targets reachable\n")
                else:
                    for target, info in network.get('targets', {}).items():
                        f.write(f"  {target}: {info.get('status', 'unknown')}\n")
                f.write("\n")

            # Processes
            if "processes" in metrics:
                processes = metrics["processes"]
                f.write(f"Monitored Applications: {len(processes.get('monitored_processes', {}))}\n")
                for app, info in processes.get('monitored_processes', {}).items():
                    f.write(f"  {app}: {info.get('status', 'unknown')}\n")
                if processes.get('critical_processes_down'):
                    f.write(f"  CRITICAL APPLICATIONS DOWN: {', '.join(processes['critical_processes_down'])}\n")
                f.write("\n")

            f.write("-"*80 + "\n")

    except Exception as e:
        logger.error(f"Error writing to summary: {e}")

def save_metrics_to_file(metrics: Dict):
    """Save detailed metrics to a JSON file."""
    try:
        # Create metrics file with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        metrics_file = LOG_DIR / f"system_metrics_{timestamp}.json"

        with open(metrics_file, 'w') as f:
            json.dump(metrics, f, indent=2, default=str)

        logger.info(f"Saved metrics to: {metrics_file}")

        # Also save to a rolling file (keeps last 7 days)
        rolling_file = LOG_DIR / "latest_metrics.json"
        with open(rolling_file, 'w') as f:
            json.dump(metrics, f, indent=2, default=str)

    except Exception as e:
        logger.error(f"Error saving metrics to file: {e}")

def get_system_info() -> Dict:
    """Get basic system information."""
    try:
        system_info = {
            "hostname": socket.gethostname(),
            "platform": platform.system(),
            "platform_version": platform.version(),
            "architecture": platform.machine(),
            "processor": platform.processor(),
            "python_version": platform.python_version(),
            "boot_time": datetime.fromtimestamp(psutil.boot_time()).isoformat(),
            "uptime": str(datetime.now() - datetime.fromtimestamp(psutil.boot_time())).split('.')[0],
        }
        return system_info
    except Exception as e:
        logger.error(f"Error getting system info: {e}")
        return {}

def check_system_health() -> Dict:
    """Perform a comprehensive system health check."""
    try:
        health_info = {
            "timestamp": datetime.now().isoformat(),
            "checks": {},
            "alerts": []
        }

        # Check CPU
        cpu_usage = check_cpu_usage()
        health_info["checks"]["cpu"] = {
            "value": cpu_usage,
            "status": "warning" if cpu_usage > CPU_THRESHOLD else "normal"
        }
        if cpu_usage > CPU_THRESHOLD:
            health_info["alerts"].append(f"High CPU usage: {cpu_usage:.1f}%")
            logger.warning(f"ALERT: High CPU usage detected: {cpu_usage:.1f}%")

        # Check memory
        memory_info = check_memory_usage()
        health_info["checks"]["memory"] = {
            "value": memory_info.get('percent', 0),
            "status": "warning" if memory_info.get('percent', 0) > MEMORY_THRESHOLD else "normal"
        }
        if memory_info.get('percent', 0) > MEMORY_THRESHOLD:
            health_info["alerts"].append(f"High memory usage: {memory_info.get('percent', 0):.1f}%")
            logger.warning(f"ALERT: High memory usage detected: {memory_info.get('percent', 0):.1f}%")

        # Check disk
        disk_info = check_disk_usage()
        disk_warnings = []
        for mountpoint, disk_data in disk_info.items():
            if disk_data.get('percent', 0) > DISK_THRESHOLD:
                disk_warnings.append(f"{mountpoint}: {disk_data.get('percent', 0):.1f}%")
                health_info["alerts"].append(f"High disk usage on {mountpoint}: {disk_data.get('percent', 0):.1f}%")

        if disk_warnings:
            logger.warning(f"ALERT: High disk usage: {', '.join(disk_warnings)}")

        health_info["checks"]["disk"] = {
            "values": {mount: data.get('percent', 0) for mount, data in disk_info.items()},
            "status": "warning" if disk_warnings else "normal"
        }

        # Check network
        network_info = check_network_connectivity()
        health_info["checks"]["network"] = {
            "overall_status": network_info.get('overall_status', 'unknown'),
            "status": "normal" if network_info.get('overall_status') == 'healthy' else "warning"
        }
        if network_info.get('overall_status') != 'healthy':
            health_info["alerts"].append(f"Network issues detected: {network_info.get('overall_status')}")
            logger.warning(f"ALERT: Network issues detected: {network_info.get('overall_status')}")

        # Check processes
        process_info = check_processes()
        health_info["checks"]["processes"] = {
            "critical_processes_down": process_info.get('critical_processes_down', []),
            "status": "critical" if process_info.get('critical_processes_down') else "normal"
        }
        if process_info.get('critical_processes_down'):
            health_info["alerts"].append(f"Critical applications down: {', '.join(process_info['critical_processes_down'])}")
            logger.error(f"ALERT: Critical applications down: {', '.join(process_info['critical_processes_down'])}")

        return health_info

    except Exception as e:
        logger.error(f"Error performing health check: {e}")
        return {"error": str(e)}

def start_monitoring():
    """Start the monitoring loop."""
    try:
        if monitoring_state["monitoring_active"]:
            logger.warning("Monitoring is already active")
            return

        monitoring_state["monitoring_active"] = True
        monitoring_state["start_time"] = datetime.now()

        logger.info("="*80)
        logger.info("SYSTEM PARAMETERS LOGGER - MONITORING STARTED")
        logger.info("="*80)
        logger.info(f"Monitoring started at: {monitoring_state['start_time'].strftime('%Y-%m-%d %H:%M:%S')}")

        # Log initial system info
        system_info = get_system_info()
        logger.info(f"System: {system_info.get('platform', 'Unknown')} {system_info.get('platform_version', '')}")
        logger.info(f"Hostname: {system_info.get('hostname', 'Unknown')}")
        logger.info(f"Uptime: {system_info.get('uptime', 'Unknown')}")

        # Create initial summary
        initial_metrics = {
            "system": system_info,
            "timestamp": datetime.now().isoformat()
        }
        write_metrics_to_summary(initial_metrics)
        save_metrics_to_file(initial_metrics)

        # Start monitoring threads
        monitoring_threads = []

        # CPU monitoring thread
        cpu_thread = threading.Thread(
            target=monitor_cpu_continuously,
            args=(CPU_CHECK_INTERVAL,),
            daemon=True
        )
        cpu_thread.start()
        monitoring_threads.append(cpu_thread)

        # Memory monitoring thread
        memory_thread = threading.Thread(
            target=monitor_memory_continuously,
            args=(MEMORY_CHECK_INTERVAL,),
            daemon=True
        )
        memory_thread.start()
        monitoring_threads.append(memory_thread)

        # Disk monitoring thread
        disk_thread = threading.Thread(
            target=monitor_disk_continuously,
            args=(DISK_CHECK_INTERVAL,),
            daemon=True
        )
        disk_thread.start()
        monitoring_threads.append(disk_thread)

        # Network monitoring thread
        network_thread = threading.Thread(
            target=monitor_network_continuously,
            args=(NETWORK_CHECK_INTERVAL,),
            daemon=True
        )
        network_thread.start()
        monitoring_threads.append(network_thread)

        # Process monitoring thread
        process_thread = threading.Thread(
            target=monitor_processes_continuously,
            args=(PROCESS_CHECK_INTERVAL,),
            daemon=True
        )
        process_thread.start()
        monitoring_threads.append(process_thread)

        # Main monitoring loop
        main_monitoring_loop()

    except Exception as e:
        logger.error(f"Error starting monitoring: {e}")
        raise

def monitor_cpu_continuously(interval: int):
    """Continuously monitor CPU usage."""
    try:
        while monitoring_state["monitoring_active"]:
            cpu_usage = check_cpu_usage()
            if cpu_usage > CPU_THRESHOLD:
                logger.warning(f"ALERT: High CPU usage detected: {cpu_usage:.1f}%")
            time.sleep(interval)
    except Exception as e:
        logger.error(f"Error in CPU monitoring thread: {e}")

def monitor_memory_continuously(interval: int):
    """Continuously monitor memory usage."""
    try:
        while monitoring_state["monitoring_active"]:
            memory_info = check_memory_usage()
            memory_percent = memory_info.get('percent', 0)
            if memory_percent > MEMORY_THRESHOLD:
                logger.warning(f"ALERT: High memory usage detected: {memory_percent:.1f}%")
            time.sleep(interval)
    except Exception as e:
        logger.error(f"Error in memory monitoring thread: {e}")

def monitor_disk_continuously(interval: int):
    """Continuously monitor disk usage."""
    try:
        while monitoring_state["monitoring_active"]:
            disk_info = check_disk_usage()
            for mountpoint, disk_data in disk_info.items():
                disk_percent = disk_data.get('percent', 0)
                if disk_percent > DISK_THRESHOLD:
                    logger.warning(f"ALERT: High disk usage on {mountpoint}: {disk_percent:.1f}%")
            time.sleep(interval)
    except Exception as e:
        logger.error(f"Error in disk monitoring thread: {e}")

def monitor_network_continuously(interval: int):
    """Continuously monitor network connectivity."""
    try:
        while monitoring_state["monitoring_active"]:
            network_info = check_network_connectivity()
            if network_info.get('overall_status') != 'healthy':
                logger.warning(f"ALERT: Network issues detected: {network_info.get('overall_status')}")
            time.sleep(interval)
    except Exception as e:
        logger.error(f"Error in network monitoring thread: {e}")

def monitor_processes_continuously(interval: int):
    """Continuously monitor processes and applications."""
    try:
        while monitoring_state["monitoring_active"]:
            process_info = check_processes()
            if process_info.get('critical_processes_down'):
                logger.error(f"ALERT: Critical applications down: {', '.join(process_info['critical_processes_down'])}")
            time.sleep(interval)
    except Exception as e:
        logger.error(f"Error in process monitoring thread: {e}")

def main_monitoring_loop():
    """Main monitoring loop that checks everything at regular intervals."""
    try:
        # Initial health check
        health_info = check_system_health()
        logger.info("Initial system health check completed")

        # Main loop
        while monitoring_state["monitoring_active"]:
            try:
                # Perform health check
                health_info = check_system_health()

                # Write to summary and save metrics
                write_metrics_to_summary(health_info)
                save_metrics_to_file(health_info)

                # Cleanup old logs
                cleanup_old_logs()

                # Sleep for main check interval (default 300 seconds)
                sleep_interval = config["monitoring"].get("cpu_check_interval", 300)
                time.sleep(sleep_interval)

            except KeyboardInterrupt:
                logger.info("Monitoring interrupted by user")
                break
            except Exception as e:
                logger.error(f"Error in main monitoring loop: {e}")
                time.sleep(60)  # Wait 1 minute before retrying

    except Exception as e:
        logger.error(f"Error in main monitoring loop: {e}")
    finally:
        monitoring_state["monitoring_active"] = False
        logger.info("="*80)
        logger.info("SYSTEM PARAMETERS LOGGER - MONITORING STOPPED")
        logger.info("="*80)

def main():
    """Main entry point for the system monitor."""
    setup_logging()

    # Parse command line arguments
    import argparse
    parser = argparse.ArgumentParser(
        description="System Parameters Logger - Monitor system health and internet connection"
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=config["monitoring"]["cpu_check_interval"],
        help="Monitoring interval in seconds"
    )
    parser.add_argument(
        "--config",
        type=str,
        help="Path to configuration file"
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="Run monitoring once and exit"
    )
    parser.add_argument(
        "--log-dir",
        type=str,
        help="Directory for log files"
    )

    args = parser.parse_args()

    # Update global config if needed
    if args.config:
        try:
            global config
            config = load_config()
            if args.config != str(CONFIG_DIR / "config.json"):
                # Load custom config
                with open(args.config, 'r') as f:
                    config = json.load(f)
                logger.info(f"Loaded custom configuration from: {args.config}")
        except Exception as e:
            logger.error(f"Could not load custom config: {e}")
            return 1

    if args.log_dir:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        logger.info(f"Using custom log directory: {args.log_dir}")

    try:
        if args.once:
            # Run once and exit
            logger.info("Running monitoring check once...")
            health_info = check_system_health()
            print(json.dumps(health_info, indent=2, default=str))
            return 0
        else:
            # Start continuous monitoring
            start_monitoring()
            return 0

    except KeyboardInterrupt:
        logger.info("Monitoring stopped by user")
        return 0
    except Exception as e:
        logger.error(f"Error in main: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())