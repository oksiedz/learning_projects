"""
remote_log_uploader.py — Remote Log Upload Module

This module provides functionality to upload system monitoring logs to
remote destinations, including GitHub releases, GitHub issues, or a
monitoring service webhook.

Upload destinations:
- GitHub Release assets (with personal access token)
- GitHub Issue comments (for attaching log summaries)
- Generic webhook (POST JSON to a monitoring service)
- Local network share (for NAS/immich server access)
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
import base64

logger = logging.getLogger(__name__)


class RemoteLogUploader:
    """
    Handles uploading monitoring logs to remote destinations.
    """

    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.github_token = self.config.get("github_token", os.environ.get("GITHUB_TOKEN", ""))
        self.github_repo = self.config.get("github_repo", os.environ.get("GITHUB_REPO", ""))
        self.webhook_url = self.config.get("webhook_url", os.environ.get("WEBHOOK_URL", ""))
        self.upload_dir = self.config.get("upload_dir", "logs")

    # ------------------------------------------------------------------
    # GitHub API helpers
    # ------------------------------------------------------------------

    def _github_headers(self) -> Dict:
        """Return headers for GitHub API requests."""
        return {
            "Authorization": f"token {self.github_token}",
            "Accept": "application/vnd.github+json",
            "User-Agent": "System-Parameters-Logger",
        }

    def github_release_exists(self, tag_name: str) -> bool:
        """Check if a GitHub release tag exists."""
        try:
            import urllib.request
            url = f"https://api.github.com/repos/{self.github_repo}/releases/tags/{tag_name}"
            req = urllib.request.Request(url, headers=self._github_headers())
            with urllib.request.urlopen(req, timeout=10) as resp:
                return resp.getcode() == 200
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return False
            raise
        except Exception as e:
            logger.error(f"Error checking GitHub release: {e}")
            return False

    def create_github_release(self, tag_name: str, release_name: str = None,
                              body: str = None) -> Optional[Dict]:
        """
        Create a new GitHub release for log archiving.

        Returns release info dict or None on failure.
        """
        try:
            import urllib.request
            url = f"https://api.github.com/repos/{self.github_repo}/releases"

            data = {
                "tag_name": tag_name,
                "name": release_name or f"Monitoring Logs {tag_name}",
                "body": body or f"System monitoring logs archived at {datetime.now().isoformat()}",
                "draft": False,
                "prerelease": False,
            }

            req = urllib.request.Request(
                url,
                data=json.dumps(data).encode('utf-8'),
                headers={**self._github_headers(), "Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=15) as resp:
                return json.loads(resp.read().decode('utf-8'))
        except Exception as e:
            logger.error(f"Error creating GitHub release: {e}")
            return None

    def upload_to_github_release(self, release_id: int, file_path: Path,
                                 file_name: str = None) -> bool:
        """
        Upload a log file as a GitHub release asset.

        Returns True on success.
        """
        try:
            import urllib.request
            url = f"https://uploads.github.com/repos/{self.github_repo}/releases/{release_id}/assets"
            file_name = file_name or file_path.name

            with open(file_path, 'rb') as f:
                file_data = f.read()

            req = urllib.request.Request(
                f"{url}?name={file_name}",
                data=file_data,
                headers={
                    **self._github_headers(),
                    "Content-Type": "application/octet-stream",
                    "Content-Length": str(len(file_data)),
                },
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                return resp.getcode() in (200, 201)
        except Exception as e:
            logger.error(f"Error uploading to GitHub release: {e}")
            return False

    def post_github_issue_comment(self, issue_number: int, body: str) -> bool:
        """
        Post a comment to a GitHub issue with log summary.

        Returns True on success.
        """
        try:
            import urllib.request
            url = f"https://api.github.com/repos/{self.github_repo}/issues/{issue_number}/comments"

            data = {"body": body}
            req = urllib.request.Request(
                url,
                data=json.dumps(data).encode('utf-8'),
                headers={**self._github_headers(), "Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=15) as resp:
                return resp.getcode() == 201
        except Exception as e:
            logger.error(f"Error posting GitHub issue comment: {e}")
            return False

    # ------------------------------------------------------------------
    # Webhook upload
    # ------------------------------------------------------------------

    def upload_to_webhook(self, payload: Dict) -> bool:
        """
        POST monitoring data to a generic webhook URL.

        Useful for sending to monitoring services, Discord, Slack, etc.
        """
        if not self.webhook_url:
            logger.warning("No webhook URL configured — skipping webhook upload")
            return False

        try:
            import urllib.request
            data = json.dumps(payload).encode('utf-8')
            req = urllib.request.Request(
                self.webhook_url,
                data=data,
                headers={"Content-Type": "application/json", "User-Agent": "System-Parameters-Logger"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=15) as resp:
                return resp.getcode() in (200, 201, 204)
        except Exception as e:
            logger.error(f"Error uploading to webhook: {e}")
            return False

    # ------------------------------------------------------------------
    # Local network share (NAS / immich server)
    # ------------------------------------------------------------------

    def upload_to_network_share(self, source_file: Path, dest_path: str = None) -> bool:
        """
        Copy log files to a network share (e.g., NAS, immich server).

        Useful when the laptop is on the same network as the server.
        """
        if dest_path is None:
            dest_path = self.config.get("network_share_path", "")

        if not dest_path:
            logger.warning("No network share path configured — skipping")
            return False

        try:
            import shutil
            dest = Path(dest_path)
            dest.mkdir(parents=True, exist_ok=True)

            dest_file = dest / source_file.name
            shutil.copy2(source_file, dest_file)
            logger.info(f"Copied {source_file} to {dest_file}")
            return True
        except Exception as e:
            logger.error(f"Error copying to network share: {e}")
            return False

    # ------------------------------------------------------------------
    # High-level upload orchestration
    # ------------------------------------------------------------------

    def upload_latest_logs(self, log_dir: Path = None,
                           include_summary: bool = True) -> Dict:
        """
        Upload the latest log files to all configured remote destinations.

        Returns a dict with per-destination success/failure status.
        """
        if log_dir is None:
            log_dir = Path(__file__).parent / "logs"

        results = {
            "timestamp": datetime.now().isoformat(),
            "github_release": False,
            "webhook": False,
            "network_share": False,
            "errors": [],
        }

        # Find latest log files
        log_files = []
        if log_dir.exists():
            log_files = sorted(
                log_dir.glob("*.log"),
                key=lambda p: p.stat().st_mtime,
                reverse=True,
            )
            # Also include metrics files
            metrics_files = sorted(
                log_dir.glob("system_metrics_*.json"),
                key=lambda p: p.stat().st_mtime,
                reverse=True,
            )
            log_files.extend(metrics_files[:3])

        if not log_files:
            results["errors"].append("No log files found to upload")
            return results

        primary_log = log_files[0]

        # GitHub release upload
        if self.github_token and self.github_repo:
            try:
                tag_name = f"monitoring-{datetime.now().strftime('%Y%m%d')}"
                if not self.github_release_exists(tag_name):
                    release = self.create_github_release(tag_name)
                    if release:
                        results["github_release"] = self.upload_to_github_release(
                            release["id"], primary_log
                        )
                    else:
                        results["errors"].append("Failed to create GitHub release")
                else:
                    # Find existing release and upload to it
                    import urllib.request
                    url = f"https://api.github.com/repos/{self.github_repo}/releases/tags/{tag_name}"
                    req = urllib.request.Request(url, headers=self._github_headers())
                    with urllib.request.urlopen(req, timeout=10) as resp:
                        release = json.loads(resp.read().decode('utf-8'))
                    results["github_release"] = self.upload_to_github_release(
                        release["id"], primary_log
                    )
            except Exception as e:
                results["errors"].append(f"GitHub upload error: {e}")

        # Webhook upload
        if self.webhook_url:
            try:
                payload = {
                    "timestamp": datetime.now().isoformat(),
                    "log_file": primary_log.name,
                    "log_size": primary_log.stat().st_size,
                    "source": "system_parameters_logger",
                }
                results["webhook"] = self.upload_to_webhook(payload)
            except Exception as e:
                results["errors"].append(f"Webhook upload error: {e}")

        # Network share upload
        network_share = self.config.get("network_share_path", "")
        if network_share:
            try:
                results["network_share"] = self.upload_to_network_share(primary_log)
            except Exception as e:
                results["errors"].append(f"Network share upload error: {e}")

        return results

    def create_heartbeat_payload(self, system_info: Dict = None,
                                 health_info: Dict = None) -> Dict:
        """
        Create a heartbeat payload for webhook/monitoring service.

        Includes system status and latest health check results.
        """
        payload = {
            "timestamp": datetime.now().isoformat(),
            "source": "system_parameters_logger",
            "hostname": system_info.get("hostname", "unknown") if system_info else "unknown",
            "platform": system_info.get("platform", "unknown") if system_info else "unknown",
            "uptime": system_info.get("uptime", "unknown") if system_info else "unknown",
        }

        if health_info:
            payload["cpu_percent"] = health_info.get("checks", {}).get("cpu", {}).get("value")
            payload["memory_percent"] = health_info.get("checks", {}).get("memory", {}).get("value")
            payload["network_status"] = health_info.get("checks", {}).get("network", {}).get("status")
            payload["overall_health"] = health_info.get("overall_status", "unknown")
            payload["alerts"] = health_info.get("alerts", [])

        return payload


def upload_logs_to_remote(log_dir: Path = None, config: Dict = None) -> Dict:
    """
    Convenience function to upload logs to all configured remote destinations.

    Returns upload results dict.
    """
    uploader = RemoteLogUploader(config)
    return uploader.upload_latest_logs(log_dir)


def send_heartbeat(system_info: Dict = None, health_info: Dict = None,
                   webhook_url: str = None) -> bool:
    """
    Send a heartbeat to a monitoring webhook.

    Returns True on success.
    """
    if not webhook_url:
        webhook_url = os.environ.get("WEBHOOK_URL", "")

    if not webhook_url:
        logger.warning("No webhook URL configured — cannot send heartbeat")
        return False

    uploader = RemoteLogUploader({"webhook_url": webhook_url})
    payload = uploader.create_heartbeat_payload(system_info, health_info)
    return uploader.upload_to_webhook(payload)


if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

    print("Remote Log Uploader Module")
    print("=" * 50)
    print(f"GitHub Token configured: {bool(os.environ.get('GITHUB_TOKEN'))}")
    print(f"GitHub Repo configured: {bool(os.environ.get('GITHUB_REPO'))}")
    print(f"Webhook URL configured: {bool(os.environ.get('WEBHOOK_URL'))}")
    print("=" * 50)
    print("Set environment variables to enable remote uploads:")
    print("  export GITHUB_TOKEN=your_token")
    print("  export GITHUB_REPO=username/repo")
    print("  export WEBHOOK_URL=https://your-webhook-endpoint")