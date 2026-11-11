# System Parameters Logger

A comprehensive system monitoring tool designed to log critical system parameters and internet connection health.

## Overview

This tool continuously monitors and logs essential system metrics including CPU usage, memory consumption, disk status, network connectivity, and system processes. It generates detailed logs that help diagnose issues when remote access becomes problematic, as in the case of an Immich server that appears fine locally but is difficult to control remotely.

## Features

- **System Metrics Monitoring**: CPU usage, memory consumption, disk space, and system uptime
- **Network Health Monitoring**: Internet connectivity status, ping tests, and network interface information
- **Process Monitoring**: Key system processes and their resource usage
- **Application Monitoring**: Custom application health checks
- **Configurable Logging**: Flexible log levels and output formats
- **Cross-Platform Support**: Windows, Linux, and macOS compatibility
- **Scheduled Reporting**: Configurable monitoring intervals
- **Alert System**: Configurable thresholds for critical values

## Requirements

- Python 3.8+
- Windows, Linux, or macOS

## Installation

1. Clone the repository
2. Navigate to the project directory
3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the main script:

```bash
python system_monitor.py
```

Or use the command-line interface:

```bash
python -m system_parameters_logger.cli
```

## Configuration

Configuration can be modified in `config.py`:

- Log directory and file settings
- Monitoring intervals
- Alert thresholds
- Network check targets
- Application monitoring settings

## Logs

All monitoring data is logged to the `logs/` directory with timestamps and detailed information about system state.

## License

This project is part of the learning projects repository.