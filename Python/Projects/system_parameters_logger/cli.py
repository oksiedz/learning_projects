"""
Command-line interface for System Parameters Logger.

This module provides a command-line interface for controlling the system monitoring tool,
including starting/stopping monitoring, viewing logs, and managing configuration.
"""

import argparse
import sys
import os
import json
import time
from pathlib import Path
import subprocess
import logging

# Add local imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from system_monitor import (
    monitoring_state,
    get_system_info,
    LOG_DIR,
    cleanup_old_logs,
)

def setup_logging():
    """Setup logging for CLI operations."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )

logger = logging.getLogger(__name__)

def start_monitoring():
    """Start the monitoring system."""
    try:
        # Import and start the monitoring system
        from system_monitor import start_monitoring as start_mon
        print("Starting System Parameters Logger...")
        print("This tool will continuously monitor system parameters and internet connection.")
        print("Press Ctrl+C to stop monitoring.\n")

        start_mon()

    except KeyboardInterrupt:
        print("\nMonitoring stopped by user")
    except Exception as e:
        print(f"Error starting monitoring: {e}")
        logger.error(f"Error starting monitoring: {e}")
        return False

    return True

def stop_monitoring():
    """Stop the monitoring system."""
    try:
        monitoring_state["monitoring_active"] = False
        print("Monitoring stopped.")
        return True
    except Exception as e:
        print(f"Error stopping monitoring: {e}")
        logger.error(f"Error stopping monitoring: {e}")
        return False

def view_logs():
    """View recent monitoring logs."""
    try:
        log_file = LOG_DIR / "system_monitor.log"

        if not log_file.exists():
            print("No log file found.")
            return

        print("\n" + "="*80)
        print("RECENT SYSTEM MONITORING LOGS")
        print("="*80)

        # Read last 100 lines
        with open(log_file, 'r') as f:
            lines = f.readlines()

        # Show last 100 lines or all if less than 100
        start_line = max(0, len(lines) - 100)
        for line in lines[start_line:]:
            print(line.rstrip())

        print("="*80)
        print(f"Showing last {len(lines) - start_line} lines from {log_file.name}")
        print("="*80)

    except Exception as e:
        print(f"Error reading logs: {e}")
        logger.error(f"Error reading logs: {e}")

def view_summary():
    """View the monitoring summary."""
    try:
        summary_file = LOG_DIR / "monitoring_summary.txt"

        if not summary_file.exists():
            print("No summary file found.")
            return

        print("\n" + "="*80)
        print("SYSTEM MONITORING SUMMARY")
        print("="*80)

        with open(summary_file, 'r') as f:
            content = f.read()

        print(content)

    except Exception as e:
        print(f"Error reading summary: {e}")
        logger.error(f"Error reading summary: {e}")

def list_metrics_files():
    """List available metrics files."""
    try:
        metrics_files = list(LOG_DIR.glob("system_metrics_*.json"))

        if not metrics_files:
            print("No metrics files found.")
            return

        print("\n" + "="*80)
        print("AVAILABLE METRICS FILES")
        print("="*80)

        for file in sorted(metrics_files, key=lambda x: x.stat().st_mtime, reverse=True):
            stat = file.stat()
            mtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stat.st_mtime))
            size = stat.st_size / 1024  # KB
            print(f"{file.name:50} {mtime:19} {size:8.1f} KB")

        print("="*80)

    except Exception as e:
        print(f"Error listing metrics files: {e}")
        logger.error(f"Error listing metrics files: {e}")

def cleanup():
    """Clean up old log files and alerts."""
    try:
        print("Cleaning up old logs...")
        cleanup_old_logs()
        print("Cleanup completed.")
        return True
    except Exception as e:
        print(f"Error during cleanup: {e}")
        logger.error(f"Error during cleanup: {e}")
        return False

def get_system_status():
    """Get current system status."""
    try:
        print("\n" + "="*80)
        print("CURRENT SYSTEM STATUS")
        print("="*80)

        system_info = get_system_info()

        print(f"Hostname: {system_info['hostname']}")
        print(f"Platform: {system_info['platform']} {system_info['platform_version']}")
        print(f"Architecture: {system_info['architecture']}")
        print(f"Processor: {system_info['processor']}")
        print(f"Python Version: {system_info['python_version']}")
        print(f"Boot Time: {system_info['boot_time']}")

        # Get current resource usage
        import psutil
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')

        print(f"\nCurrent Resource Usage:")
        print(f"  CPU: {cpu_percent}%")
        print(f"  Memory: {memory.percent}% ({memory.used/(1024**3):.2f}GB / {memory.total/(1024**3):.2f}GB)")
        print(f"  Disk: {disk.percent}% ({disk.used/(1024**3):.2f}GB / {disk.total/(1024**3):.2f}GB)")

        # Get network stats
        net_io = psutil.net_io_counters()
        print(f"\nNetwork I/O:")
        print(f"  Sent: {net_io.bytes_sent/(1024**2):.2f}MB")
        print(f"  Received: {net_io.bytes_recv/(1024**2):.2f}MB")
        print(f"  Packets: {net_io.packets_sent + net_io.packets_recv}")

        print("="*80)

    except Exception as e:
        print(f"Error getting system status: {e}")
        logger.error(f"Error getting system status: {e}")

def run_pinging_test():
    """Run a network pinging test."""
    try:
        print("\nRunning network pinging test...")

        targets = ["8.8.8.8", "1.1.1.1", "google.com", "cloudflare.com"]

        for target in targets:
            try:
                print(f"Pinging {target}...")
                result = subprocess.run(
                    ["ping", "-c", "4", "-W", "5", target],
                    capture_output=True,
                    text=True,
                    timeout=30
                )

                if result.returncode == 0:
                    print(f"  ✓ {target}: Success")
                    for line in result.stdout.split('\n'):
                        if "avg" in line:
                            parts = line.split('/')
                            if len(parts) >= 4:
                                avg_time = float(parts[3])
                                print(f"    Average time: {avg_time}ms")
                                break
                else:
                    print(f"  ✗ {target}: Failed (exit code {result.returncode})")
                    if result.stderr:
                        print(f"    Error: {result.stderr.strip()}")

            except subprocess.TimeoutExpired:
                print(f"  ✗ {target}: Timeout")
            except Exception as e:
                print(f"  ✗ {target}: Error - {e}")

        print("\nPing test completed.")

    except Exception as e:
        print(f"Error running pinging test: {e}")
        logger.error(f"Error running pinging test: {e}")

def main():
    """Main CLI entry point."""
    setup_logging()

    parser = argparse.ArgumentParser(
        description="System Parameters Logger - Monitor system health and internet connection"
    )

    parser.add_argument(
        "action",
        choices=["start", "stop", "view-logs", "view-summary", "list-metrics", "cleanup", "status", "ping"],
        help="Action to perform"
    )

    parser.add_argument(
        "--log-dir",
        default=str(LOG_DIR),
        help="Directory for log files"
    )

    parser.add_argument(
        "--interval",
        type=int,
        default=300,
        help="Monitoring interval in seconds (for start action)"
    )

    args = parser.parse_args()

    # Route to appropriate function based on action
    actions = {
        "start": start_monitoring,
        "stop": stop_monitoring,
        "view-logs": view_logs,
        "view-summary": view_summary,
        "list-metrics": list_metrics_files,
        "cleanup": cleanup,
        "status": get_system_status,
        "ping": run_pinging_test,
    }

    if args.action in actions:
        actions[args.action]()
    else:
        parser.print_help()
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())