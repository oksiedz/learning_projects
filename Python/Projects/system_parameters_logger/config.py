"""
Configuration module for System Parameters Logger.

This module contains all configurable settings for the system monitoring tool,
including logging settings, monitoring intervals, alert thresholds, and
network monitoring configurations.
"""

import os
from pathlib import Path
from dataclasses import dataclass
from typing import List, Optional
import json

# Base directories
BASE_DIR = Path(__file__).parent.absolute()
LOG_DIR = BASE_DIR / "logs"
CONFIG_DIR = BASE_DIR / "config"

# Create directories if they don't exist
LOG_DIR.mkdir(exist_ok=True)
CONFIG_DIR.mkdir(exist_ok=True)

# Default configuration
DEFAULT_CONFIG = {
    "monitoring": {
        "cpu_check_interval": 60,  # seconds
        "memory_check_interval": 60,
        "disk_check_interval": 300,
        "network_check_interval": 30,
        "process_check_interval": 120,
        "log_retention_days": 30,
        "max_log_size_mb": 100,
    },
    "alerts": {
        "cpu_threshold": 90,  # percentage
        "memory_threshold": 85,  # percentage
        "disk_threshold": 90,  # percentage
        "ping_threshold": 1000,  # milliseconds
        "process_restart_threshold": 300,  # seconds
    },
    "network": {
        "ping_targets": [
            "8.8.8.8",
            "1.1.1.1",
            "google.com",
            "cloudflare.com"
        ],
        "dns_servers": [
            "8.8.8.8",
            "1.1.1.1",
            "208.67.222.222"
        ],
        "connection_timeout": 10,  # seconds
    },
    "applications": [
        {
            "name": "Immich Server",
            "process_name": "immich",
            "check_interval": 60,
            "critical": True,
            "restart_if_down": True,
        },
        {
            "name": "File System",
            "path": "C:/",
            "check_interval": 300,
            "critical": True,
        },
    ],
    "logging": {
        "level": "INFO",  # DEBUG, INFO, WARNING, ERROR, CRITICAL
        "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        "console_output": True,
        "file_output": True,
        "log_file": "system_monitor.log",
    }
}

# Load configuration from file if it exists
CONFIG_FILE = CONFIG_DIR / "config.json"

def load_config():
    """Load configuration from file or return default config."""
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not load config file: {e}")
            print("Using default configuration.")
    return DEFAULT_CONFIG.copy()

# Global configuration instance
config = load_config()

# Save configuration to file
def save_config():
    """Save current configuration to file."""
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
    except IOError as e:
        print(f"Warning: Could not save config file: {e}")

# Custom logger configuration
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "detailed": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        },
        "simple": {
            "format": "%(asctime)s - %(levelname)s - %(message)s",
            "datefmt": "%H:%M:%S"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "detailed" if config["logging"]["level"] == "DEBUG" else "simple",
            "level": config["logging"]["level"]
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "detailed",
            "level": config["logging"]["level"],
            "filename": LOG_DIR / config["logging"]["log_file"],
            "maxBytes": config["logging"]["max_log_size_mb"] * 1024 * 1024,
            "backupCount": 5,
        }
    },
    "root": {
        "handlers": ["console", "file"],
        "level": config["logging"]["level"]
    }
}

# Network monitoring configuration
PING_TIMEOUT = config["network"]["connection_timeout"]
PING_COUNT = 4
DNS_SERVERS = config["network"]["dns_servers"]

# Alert thresholds
CPU_THRESHOLD = config["alerts"]["cpu_threshold"]
MEMORY_THRESHOLD = config["alerts"]["memory_threshold"]
DISK_THRESHOLD = config["alerts"]["disk_threshold"]
PING_THRESHOLD = config["alerts"]["ping_threshold"]

# Monitoring intervals
CPU_CHECK_INTERVAL = config["monitoring"]["cpu_check_interval"]
MEMORY_CHECK_INTERVAL = config["monitoring"]["memory_check_interval"]
DISK_CHECK_INTERVAL = config["monitoring"]["disk_check_interval"]
NETWORK_CHECK_INTERVAL = config["monitoring"]["network_check_interval"]
PROCESS_CHECK_INTERVAL = config["monitoring"]["process_check_interval"]

# Application monitoring
MONITORED_APPLICATIONS = config["applications"]