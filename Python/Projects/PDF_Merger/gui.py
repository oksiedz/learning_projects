from __future__ import annotations

import logging
import sys
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from .app import add_unique_files, collect_supported_files

LOGGER = logging.getLogger("offline_pdf_merger.gui")


class MergeWindow(QMainWindow):
    """Qt-based GUI for selecting and ordering local PDF and image files."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Offline PDF & Image Merger")
        self.resize(880, 650)
        self.setMinimumSize(680, 500)
        self.selected_files: list[str] = []

        self._build_ui()
        self._refresh_list()

    def _build_ui(self) -> None:
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)

        toolbar = QHBoxLayout()
        toolbar.setSpacing(8)
        self.add_files_button = QPushButton("Add files")
        self.add_files_button.clicked.connect(self._add_files)
        self.add_folder_button = QPushButton("Add folder")
        self.add_folder_button.clicked.connect(self._add_folder)
        self.remove_button = QPushButton("Remove selected")
        self.remove_button.clicked.connect(self._remove_selected)
        self.move_up_button = QPushButton("Move up")
        self.move_up_button.clicked.connect(self._move_up)
        self.move_down_button = QPushButton("Move down")
        self.move_down_button.clicked.connect(self._move_down)

        toolbar.addWidget(self.add_files_button)
        toolbar.addWidget(self.add_folder_button)
        toolbar.addWidget(self.remove_button)
        toolbar.addWidget(self.move_up_button)
        toolbar.addWidget(self.move_down_button)
        toolbar.addStretch()
        layout.addLayout(toolbar)

        self.file_header = QLabel("Selected files")
        self.file_header.setStyleSheet("font-weight: bold; font-size: 12px;")
        layout.addWidget(self.file_header)

        self.file_list = QListWidget()
        self.file_list.setSelectionMode(QListWidget.ExtendedSelection)
        self.file_list.doubleClicked.connect(self._show_file_details)
        layout.addWidget(self.file_list, 1)

        self.status_label = QLabel("No files selected yet.")
        self.status_label.setStyleSheet("background-color: #eef7ee; padding: 8px;")
        layout.addWidget(self.status_label)

        merge_button = QPushButton("Merge to PDF")
        merge_button.setStyleSheet("background-color: #2e7d32; color: white; padding: 10px 20px;")
        merge_button.clicked.connect(self._merge_to_pdf)
        merge_layout = QHBoxLayout()
        merge_layout.addStretch()
        merge_layout.addWidget(merge_button)
        layout.addLayout(merge_layout)

    def _add_files(self) -> None:
        LOGGER.info("Add files dialog opened")
        paths, _ = QFileDialog.getOpenFileNames(
            self,
            "Select PDF and image files",
            "/Users/tom/Downloads",
            "PDF and image files (*.pdf *.png *.jpg *.jpeg *.bmp *.gif *.tif *.tiff *.webp *.heic)",
        )
        if not paths:
            LOGGER.info("Add files dialog cancelled")
            return

        self._append_paths(paths)

    def _add_folder(self) -> None:
        LOGGER.info("Add folder dialog opened")
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select a folder containing PDF or image files",
            "/Users/tom/Downloads",
        )
        if not folder:
            LOGGER.info("Add folder dialog cancelled")
            return

        try:
            paths = [str(path) for path in collect_supported_files(folder)]
        except (OSError, ValueError) as exc:
            LOGGER.exception("Could not read selected folder: %s", exc)
            self._show_error("Folder import failed", str(exc))
            return

        LOGGER.info("Selected folder: %s; found %d supported file(s)", folder, len(paths))
        self._append_paths(paths)

    def _append_paths(self, paths: list[str]) -> None:
        new_paths = add_unique_files(self.selected_files, paths)
        if new_paths == self.selected_files:
            LOGGER.info("No new files added")
            return

        self.selected_files = new_paths
        self._refresh_list()
        LOGGER.info("List updated with %d file(s)", len(self.selected_files))

    def _refresh_list(self) -> None:
        self.file_list.clear()
        for path in self.selected_files:
            item = QListWidgetItem(Path(path).name)
            item.setData(Qt.UserRole, path)
            self.file_list.addItem(item)
        self.status_label.setText(
            f"{len(self.selected_files)} file(s) selected. Use the buttons to reorder them."
        )
        LOGGER.info("Listbox rendered %d item(s)", self.file_list.count())

    def _remove_selected(self) -> None:
        selected = [self.file_list.item(index) for index in range(self.file_list.count()) if self.file_list.item(index).isSelected()]
        if not selected:
            self._show_message("No files selected", "Select one or more files first.")
            return

        for item in selected:
            self.selected_files.remove(str(item.data(Qt.UserRole)))
        self._refresh_list()

    def _move_up(self) -> None:
        selected_rows = [index for index in range(self.file_list.count()) if self.file_list.item(index).isSelected()]
        if not selected_rows:
            self._show_message("Nothing selected", "Select one or more files first.")
            return
        for index in reversed(selected_rows):
            if index == 0:
                continue
            self.selected_files[index - 1], self.selected_files[index] = (
                self.selected_files[index],
                self.selected_files[index - 1],
            )
        self._refresh_list()
        self._restore_selection(selected_rows)

    def _move_down(self) -> None:
        selected_rows = [index for index in range(self.file_list.count()) if self.file_list.count() and self.file_list.item(index).isSelected()]
        if not selected_rows:
            self._show_message("Nothing selected", "Select one or more files first.")
            return
        for index in reversed(selected_rows):
            if index >= len(self.selected_files) - 1:
                continue
            self.selected_files[index], self.selected_files[index + 1] = (
                self.selected_files[index + 1],
                self.selected_files[index],
            )
        self._refresh_list()
        self._restore_selection(selected_rows)

    def _restore_selection(self, selected_rows: list[int]) -> None:
        for index in selected_rows:
            if index < self.file_list.count():
                self.file_list.item(index).setSelected(True)

    def _show_file_details(self, _index: int) -> None:
        item = self.file_list.currentItem()
        if item is not None:
            self._show_message("Selected file", str(item.data(Qt.UserRole)))

    def _merge_to_pdf(self) -> None:
        if not self.selected_files:
            self._show_message("No files selected", "Add at least one PDF or image first.")
            return

        output_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save merged PDF",
            "/Users/tom/Downloads/merged.pdf",
            "PDF files (*.pdf)",
        )
        if not output_path:
            return

        try:
            from .app import merge_files_to_pdf

            output = merge_files_to_pdf(self.selected_files, output_path)
            LOGGER.info("Merge completed: %s", output)
            self._show_message("Merge complete", f"Created:\n{output}")
        except Exception as exc:
            LOGGER.exception("Merge failed: %s", exc)
            self._show_error("Merge failed", str(exc))

    def _show_message(self, title: str, message: str) -> None:
        QMessageBox.information(self, title, message)

    def _show_error(self, title: str, message: str) -> None:
        QMessageBox.critical(self, title, message)


def launch_gui() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        stream=sys.stderr,
    )
    LOGGER.info("Offline PDF merger GUI started")
    application = QApplication.instance() or QApplication(sys.argv)
    window = MergeWindow()
    window.show()
    window.raise_()
    window.activateWindow()
    application.exec()
    LOGGER.info("Offline PDF merger GUI stopped")


if __name__ == "__main__":
    launch_gui()
