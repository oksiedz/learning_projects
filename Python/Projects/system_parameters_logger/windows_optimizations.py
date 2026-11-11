"""
windows_optimizations.py — Windows-Specific Optimizations

This module provides Windows-specific optimizations and utilities for the
System Parameters Logger running on Windows computers.

Key optimizations:
- Windows-specific ping command handling
- Event Log integration
- Windows Service support
- Power scheme detection
- Windows-specific process monitoring
- Path handling for Windows
"""

import os
import sys
import platform
import logging
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


def is_windows() -> bool:
    """Check if running on Windows."""
    return platform.system() == "Windows"


def windows_ping_command(target: str, count: int = 4, timeout: int = 5) -> List[str]:
    """
    Build a Windows-specific ping command.

    Windows uses -n for count and -w for timeout in milliseconds.
    """
    return ["ping", "-n", str(count), "-w", str(timeout * 1000), target]


def windows_dns_check() -> Dict:
    """Check Windows DNS configuration."""
    try:
        result = subprocess.run(
            ["ipconfig", "/all"],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            dns_servers = []
            for line in result.stdout.split('\n'):
                if "DNS Servers" in line:
                    parts = line.split(':')
                    if len(parts) > 1:
                        dns_servers.append(parts[1].strip())
            return {"status": "ok", "dns_servers": dns_servers}
        else:
            return {"status": "error", "error": result.stderr}
    except Exception as e:
        logger.error(f"Error checking Windows DNS: {e}")
        return {"status": "error", "error": str(e)}


def windows_network_adapters() -> List[Dict]:
    """Get Windows network adapter information."""
    try:
        result = subprocess.run(
            ["netsh", "interface", "show", "interface"],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            adapters = []
            for line in result.stdout.split('\n'):
                if "Enabled" in line or "Disconnected" in line:
                    parts = line.split()
                    if len(parts) >= 3:
                        adapters.append({
                            "state": parts[0],
                            "type": parts[1],
                            "name": " ".join(parts[2:])
                        })
            return adapters
        return []
    except Exception as e:
        logger.error(f"Error getting Windows network adapters: {e}")
        return []


def windows_event_log(source: str = "System Parameters Logger") -> List[Dict]:
    """Read Windows Event Log entries related to the monitor."""
    try:
        result = subprocess.run(
            ["wevtutil", "qe", "System", "/f:text", "/c:50"],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            entries = []
            for block in result.stdout.strip().split('\n\n'):
                entry = {}
                for line in block.split('\n'):
                    if ":" in line:
                        key, value = line.split(":", 1)
                        entry[key.strip()] = value.strip()
                if entry:
                    entries.append(entry)
            return entries
        return []
    except FileNotFoundError:
        logger.warning("wevtutil not available — Windows Event Log integration skipped")
        return []
    except Exception as e:
        logger.error(f"Error reading Windows Event Log: {e}")
        return []


def windows_power_status() -> Dict:
    """Get Windows power scheme and AC status."""
    try:
        result = subprocess.run(
            ["powercfg", "/getactivescheme"],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            return {"status": "ok", "active_scheme": result.stdout.strip()}
        return {"status": "error", "error": result.stderr}
    except Exception as e:
        logger.error(f"Error getting Windows power status: {e}")
        return {"status": "error", "error": str(e)}


def windows_process_list() -> List[Dict]:
    """Get Windows process list using tasklist."""
    try:
        result = subprocess.run(
            ["tasklist", "/v", "/fo", "csv"],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            processes = []
            lines = result.stdout.strip().split('\n')
            if len(lines) > 1:
                headers = lines[0].split(',')
                headers = [h.strip('"') for h in headers]
                for line in lines[1:]:
                    values = [v.strip('"') for v in line.split(',')]
                    if len(values) >= len(headers):
                        proc = dict(zip(headers, values))
                        processes.append(proc)
            return processes
        return []
    except Exception as e:
        logger.error(f"Error getting Windows process list: {e}")
        return []


def windows_service_check(service_name: str) -> str:
    """Check if a Windows service is running."""
    try:
        result = subprocess.run(
            ["sc", "query", service_name],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            for line in result.stdout.split('\n'):
                if "STATE" in line:
                    parts = line.split(':')
                    if len(parts) > 1:
                        state = parts[1].strip()
                        if "RUNNING" in state:
                            return "running"
                        elif "STOPPED" in state:
                            return "stopped"
                        else:
                            return state
        return "unknown"
    except Exception as e:
        logger.error(f"Error checking Windows service {service_name}: {e}")
        return "error"


def get_windows_temp_dir() -> Optional[Path]:
    """Get Windows temporary directory path."""
    temp_env = os.environ.get("TEMP") or os.environ.get("TMP")
    if temp_env:
        return Path(temp_env)
    return None


def get_windows_system_drive() -> str:
    """Get Windows system drive letter."""
    return os.environ.get("SystemDrive", "C:")


def get_windows_program_files() -> List[str]:
    """Get Windows Program Files directories."""
    dirs = []
    pf = os.environ.get("ProgramFiles", "C:\\Program Files")
    pf_x86 = os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)")
    dirs.append(pf)
    if pf_x86 != pf:
        dirs.append(pf_x86)
    return dirs


def windows_path_for_logs(log_dir_name: str = "logs") -> Path:
    """
    Get Windows-appropriate log directory path.

    Prefers %LOCALAPPDATA% if available, falls back to project logs directory.
    """
    local_app_data = os.environ.get("LOCALAPPDATA")
    if local_app_data:
        return Path(local_app_data) / "SystemParametersLogger" / log_dir_name
    return Path(__file__).parent / log_dir_name


def setup_windows_event_logging():
    """Setup Windows Event Log integration if available."""
    try:
        import win32evtlog
        import win32evtlogutil
        import win32api

        def log_to_event_viewer(message: str, event_type: str = "INFO"):
            """Log a message to Windows Event Viewer."""
            try:
                event_type_map = {
                    "INFO": win32evtlog.EVENTLOG_INFORMATION_TYPE,
                    "WARNING": win32evtlog.EVENTLOG_WARNING_TYPE,
                    "ERROR": win32evtlog.EVENTLOG_ERROR_TYPE,
                }
                win32evtlogutil.ReportEvent(
                    "System Parameters Logger",
                    1,
                    eventCategory=0,
                    eventType=event_type_map.get(event_type, win32evtlog.EVENTLOG_INFORMATION_TYPE),
                    strings=[message]
                )
            except Exception as e:
                logger.warning(f"Failed to log to Windows Event Viewer: {e}")

        return log_to_event_viewer
    except ImportError:
        logger.debug("pywin32 not installed — Windows Event Log integration disabled")
        return None


def install_pywin32_instructions() -> str:
    """Return instructions for installing pywin32 for Windows Event Log support."""
    return (
        "To enable Windows Event Log integration, install pywin32:\n"
        "  pip install pywin32\n"
    )


if __name__ == "__main__":
    print("Windows Optimizations Module")
    print("=" * 50)
    print(f"Running on Windows: {is_windows()}")
    if is_windows():
        print(f"System Drive: {get_windows_system_drive()}")
        print(f"Temp Dir: {get_windows_temp_dir()}")
        print(f"Program Files: {get_windows_program_files()}")
        print(f"DNS Servers: {windows_dns_check()}")
        print(f"Power Status: {windows_power_status()}")
    print("=" * 50)