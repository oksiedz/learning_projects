from __future__ import annotations

import logging
import os
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

from PIL import Image
from pypdf import PdfReader, PdfWriter
from pillow_heif import register_heif_opener
import tkinter as tk
from tkinter import filedialog, messagebox

register_heif_opener()

SUPPORTED_IMAGE_SUFFIXES = {
    ".png",
    ".jpg",
    ".jpeg",
    ".bmp",
    ".gif",
    ".tif",
    ".tiff",
    ".webp",
    ".heic",
}
SUPPORTED_SUFFIXES = {".pdf"} | SUPPORTED_IMAGE_SUFFIXES

LOGGER = logging.getLogger("offline_pdf_merger")


@dataclass(frozen=True)
class MergeItem:
    source: Path
    kind: str

    @classmethod
    def from_path(cls, path: str | os.PathLike[str]) -> "MergeItem":
        file_path = Path(path)
        if not file_path.exists() or not file_path.is_file():
            raise FileNotFoundError(f"File does not exist: {file_path}")

        suffix = file_path.suffix.lower()
        if suffix == ".pdf":
            return cls(source=file_path, kind="pdf")
        if suffix in SUPPORTED_IMAGE_SUFFIXES:
            return cls(source=file_path, kind="image")
        raise ValueError(f"Unsupported file type for {file_path.name}: {suffix}")


def build_merge_plan(files: Sequence[str | os.PathLike[str]]) -> list[MergeItem]:
    """Validate and normalize the file list while preserving the selected order."""
    plan: list[MergeItem] = []
    for file_name in files:
        plan.append(MergeItem.from_path(file_name))
    return plan


def add_unique_files(selected: Sequence[str], incoming: Sequence[str]) -> list[str]:
    """Append new file paths while preserving the existing order and avoiding duplicates."""
    result = list(selected)
    for file_name in incoming:
        if file_name not in result:
            result.append(file_name)
    return result


def collect_supported_files(folder: str | os.PathLike[str]) -> list[Path]:
    """Return supported files from a folder in deterministic filename order."""
    folder_path = Path(folder)
    if not folder_path.exists() or not folder_path.is_dir():
        raise NotADirectoryError(f"Folder does not exist: {folder_path}")

    return sorted(
        (
            path
            for path in folder_path.iterdir()
            if path.is_file() and path.suffix.lower() in SUPPORTED_SUFFIXES
        ),
        key=lambda path: (path.name.casefold(), path.name),
    )


def _append_pdf(writer: PdfWriter, source_path: Path) -> None:
    with source_path.open("rb") as source_file:
        reader = PdfReader(source_file)
        writer.append(reader)


def _append_image(writer: PdfWriter, source_path: Path) -> None:
    with Image.open(source_path) as image:
        rgb_image = image.convert("RGB")
        temp_pdf = tempfile.NamedTemporaryFile(prefix="merge_", suffix=".pdf", delete=False)
        temp_path = Path(temp_pdf.name)
        temp_pdf.close()

        try:
            rgb_image.save(temp_path, format="PDF", resolution=300.0)
            _append_pdf(writer, temp_path)
        finally:
            temp_path.unlink(missing_ok=True)


def merge_files_to_pdf(
    files: Sequence[str | os.PathLike[str]],
    destination: str | os.PathLike[str],
) -> Path:
    """Merge PDFs and images into a single PDF in the exact user-selected order."""
    if not files:
        raise ValueError("At least one file is required to create a merged PDF.")

    output_path = Path(destination)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    writer = PdfWriter()
    for item in build_merge_plan(files):
        if item.kind == "pdf":
            _append_pdf(writer, item.source)
        else:
            _append_image(writer, item.source)

    with output_path.open("wb") as output_file:
        writer.write(output_file)

    return output_path


class OfflineMergeApp(tk.Tk):
    """Simple offline GUI for ordering and merging PDF/image files."""

    def __init__(self) -> None:
        super().__init__()
        self.title("Offline PDF & Image Merger")
        self.geometry("760x560")
        self.minsize(620, 460)
        self.resizable(True, True)
        self.deiconify()
        self.selected_files: list[str] = []

        self._build_widgets()
        self.after(250, self._log_mapped_geometry)

    def _log_mapped_geometry(self) -> None:
        main_frame = self.main_frame
        listbox = next(
            (child for child in main_frame.winfo_children() if isinstance(child, tk.Listbox)),
            None,
        )
        LOGGER.info(
            "Mapped geometry: window=%sx%s main=%sx%s listbox=%sx%s",
            self.winfo_width(),
            self.winfo_height(),
            main_frame.winfo_width(),
            main_frame.winfo_height(),
            listbox.winfo_width() if listbox else 0,
            listbox.winfo_height() if listbox else 0,
        )

    def _build_widgets(self) -> None:
        main_frame = tk.Frame(self, padx=12, pady=12)
        main_frame.pack(fill=tk.BOTH, expand=True)
        self.main_frame = main_frame

        toolbar = tk.Frame(main_frame)
        toolbar.pack(fill=tk.X, pady=(0, 8))

        add_button = tk.Button(toolbar, text="Add files", command=self._add_files)
        add_button.pack(side=tk.LEFT, padx=(0, 8))

        folder_button = tk.Button(toolbar, text="Add folder", command=self._add_folder)
        folder_button.pack(side=tk.LEFT, padx=(0, 8))

        remove_button = tk.Button(toolbar, text="Remove selected", command=self._remove_selected)
        remove_button.pack(side=tk.LEFT, padx=(0, 8))

        up_button = tk.Button(toolbar, text="Move up", command=self._move_up)
        up_button.pack(side=tk.LEFT, padx=(0, 8))

        down_button = tk.Button(toolbar, text="Move down", command=self._move_down)
        down_button.pack(side=tk.LEFT)

        file_header = tk.Label(
            main_frame,
            text="Selected files",
            font=("TkDefaultFont", 10, "bold"),
            anchor="w",
        )
        file_header.pack(fill=tk.X, pady=(8, 0))

        self.listbox = tk.Listbox(
            main_frame,
            selectmode=tk.EXTENDED,
            height=20,
            bg="white",
            fg="black",
            relief="solid",
            bd=1,
        )
        self.listbox.pack(fill=tk.BOTH, expand=True, pady=(4, 0))
        self.listbox.bind("<<ListboxSelect>>", self._update_status)
        self.update_idletasks()
        LOGGER.info(
            "Listbox geometry: width=%s height=%s; parent width=%s height=%s",
            self.listbox.winfo_width(),
            self.listbox.winfo_height(),
            main_frame.winfo_width(),
            main_frame.winfo_height(),
        )

        self.status_var = tk.StringVar(value="No files selected yet.")
        status = tk.Label(main_frame, textvariable=self.status_var, anchor="w")
        status.pack(fill=tk.X, pady=(8, 0))

        action_bar = tk.Frame(main_frame)
        action_bar.pack(fill=tk.X, pady=(10, 0))

        merge_button = tk.Button(
            action_bar,
            text="Merge to PDF",
            command=self._merge_to_pdf,
            width=18,
            bg="#d9f2d9",
            font=("TkDefaultFont", 10, "bold"),
        )
        merge_button.pack(side=tk.RIGHT)

    def _update_status(self, _event: object | None = None) -> None:
        count = len(self.selected_files)
        if count == 0:
            self.status_var.set("No files selected yet.")
        else:
            self.status_var.set(f"{count} file(s) selected. Order is important.")

    def _add_files(self) -> None:
        LOGGER.info("Add files dialog opened")
        try:
            chosen_files = filedialog.askopenfilenames(
                parent=self,
                title="Select PDF and image files",
                filetypes=[
                    (
                        "PDF and image files",
                        "*.pdf *.png *.jpg *.jpeg *.bmp *.gif *.tif *.tiff *.webp *.heic",
                    ),
                    ("PDF files", "*.pdf"),
                    (
                        "Image files",
                        "*.png *.jpg *.jpeg *.bmp *.gif *.tif *.tiff *.webp *.heic",
                    ),
                ],
            )
        except Exception as exc:  # pragma: no cover - native Tk dialog errors
            LOGGER.exception("Add files dialog failed: %s", exc)
            messagebox.showerror("File selection failed", f"Could not open the file chooser:\n{exc}")
            return

        LOGGER.info("Add files dialog returned %d path(s)", len(chosen_files))
        for file_name in chosen_files:
            LOGGER.debug("Selected file: %s", file_name)

        if not chosen_files:
            LOGGER.info("Add files dialog was cancelled")
            return

        self.selected_files = add_unique_files(self.selected_files, chosen_files)
        self._refresh_listbox()
        self._update_status()
        LOGGER.info("List updated with %d file(s)", len(self.selected_files))

    def _add_folder(self) -> None:
        LOGGER.info("Add folder dialog opened")
        try:
            folder = filedialog.askdirectory(
                parent=self,
                title="Select a folder containing PDF or image files",
                initialdir="/Users/tom/Downloads",
            )
        except Exception as exc:  # pragma: no cover - native Tk dialog errors
            LOGGER.exception("Add folder dialog failed: %s", exc)
            messagebox.showerror("Folder selection failed", f"Could not open the folder chooser:\n{exc}")
            return

        if not folder:
            LOGGER.info("Add folder dialog was cancelled")
            return

        LOGGER.info("Selected folder: %s", folder)
        try:
            folder_files = collect_supported_files(folder)
        except (OSError, ValueError) as exc:
            LOGGER.exception("Could not read selected folder: %s", exc)
            messagebox.showerror("Folder import failed", f"Could not read the selected folder:\n{exc}")
            return

        LOGGER.info("Found %d supported file(s) in folder", len(folder_files))
        if not folder_files:
            messagebox.showinfo("No supported files", "The selected folder contains no PDF or image files.")
            return

        self.selected_files = add_unique_files(
            self.selected_files,
            [str(file_name) for file_name in folder_files],
        )

        self._refresh_listbox()
        self._update_status()
        self.status_var.set(
            f"Added {len(folder_files)} file(s) from {Path(folder).name}. "
            f"Use Move up/Move down to define the order."
        )

    def _refresh_listbox(self) -> None:
        self.listbox.configure(state="normal")
        self.listbox.delete(0, tk.END)
        for file_name in self.selected_files:
            self.listbox.insert(tk.END, Path(file_name).name)
        self.listbox.see(0)
        self.update_idletasks()
        rendered_count = self.listbox.size()
        LOGGER.info("Listbox rendered %d item(s)", rendered_count)

    def _remove_selected(self) -> None:
        selected_indexes = self.listbox.curselection()
        if not selected_indexes:
            return

        new_files: list[str] = []
        for index, file_name in enumerate(self.selected_files):
            if index not in selected_indexes:
                new_files.append(file_name)
        self.selected_files = new_files
        self._refresh_listbox()
        self._update_status()

    def _move_up(self) -> None:
        selected_indexes = list(self.listbox.curselection())
        if not selected_indexes:
            return

        for idx in selected_indexes:
            if idx == 0:
                continue
            self.selected_files[idx - 1], self.selected_files[idx] = (
                self.selected_files[idx],
                self.selected_files[idx - 1],
            )
        self._refresh_listbox()
        self._reselect_indexes(selected_indexes, direction=-1)

    def _move_down(self) -> None:
        selected_indexes = list(self.listbox.curselection())
        if not selected_indexes:
            return

        for idx in reversed(selected_indexes):
            if idx >= len(self.selected_files) - 1:
                continue
            self.selected_files[idx], self.selected_files[idx + 1] = (
                self.selected_files[idx + 1],
                self.selected_files[idx],
            )
        self._refresh_listbox()
        self._reselect_indexes(selected_indexes, direction=1)

    def _reselect_indexes(self, original_indexes: list[int], direction: int) -> None:
        if not original_indexes:
            return
        new_indexes = [idx + direction for idx in original_indexes]
        self.listbox.selection_clear(0, tk.END)
        for idx in new_indexes:
            if 0 <= idx < len(self.selected_files):
                self.listbox.selection_set(idx)

    def _merge_to_pdf(self) -> None:
        if not self.selected_files:
            messagebox.showwarning("No files", "Please add at least one PDF or image before merging.")
            return

        output_path = filedialog.asksaveasfilename(
            title="Save merged PDF",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
        )
        if not output_path:
            return

        try:
            merge_files_to_pdf(self.selected_files, output_path)
        except Exception as exc:  # pragma: no cover - GUI-side error handling
            messagebox.showerror("Merge failed", f"Could not create the merged PDF:\n{exc}")
            return

        messagebox.showinfo(
            "Success",
            f"Merged PDF created successfully:\n{output_path}",
        )


def launch_gui() -> None:
    from .gui import launch_gui as launch_qt_gui

    launch_qt_gui()


if __name__ == "__main__":
    launch_gui()
