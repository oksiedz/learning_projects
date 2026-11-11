"""
run_monitor.py — Entry Point Script for System Parameters Logger

This is the main entry point script for launching the System Parameters Logger.
It provides a simple command-line interface to start, stop, and manage the
system monitoring tool.

Usage:
    python run_monitor.py start
    python run_monitor.py stop
    python run_monitor.py status
    python run_monitor.py ping
    python run_monitor.py view-logs
    python run_monitor.py --help
"""

import os
import sys
from pathlib import Path

# Ensure project directory is on path
PROJECT_DIR = Path(__file__).parent.absolute()
sys.path.insert(0, str(PROJECT_DIR))

def main():
    """Main entry point."""
    from cli import main as cli_main
    return cli_main()

if __name__ == "__main__":
    sys.exit(main())