from __future__ import annotations

import tempfile
from pathlib import Path

from pypdf import PdfReader

from PDF_Merger.app import (
    add_unique_files,
    build_merge_plan,
    collect_supported_files,
    merge_files_to_pdf,
)


def test_add_unique_files_appends_new_files_after_folder_import() -> None:
    selected = ["/tmp/Photos-1-001/1.jpg"]

    updated = add_unique_files(selected, ["/tmp/Photos-1-001/2.jpg", "/tmp/Photos-1-001/1.jpg"])

    assert updated == ["/tmp/Photos-1-001/1.jpg", "/tmp/Photos-1-001/2.jpg"]


def test_collect_supported_files_returns_sorted_supported_files() -> None:
    with tempfile.TemporaryDirectory() as tmp_dir:
        folder = Path(tmp_dir)
        (folder / "b.jpg").write_bytes(b"image")
        (folder / "a.pdf").write_bytes(b"pdf")
        (folder / "ignored.txt").write_text("ignored")

        collected = collect_supported_files(folder)

        assert collected == [folder / "a.pdf", folder / "b.jpg"]


def test_heic_files_are_supported_for_folder_import_and_merge_plan() -> None:
    with tempfile.TemporaryDirectory() as tmp_dir:
        folder = Path(tmp_dir)
        heic_path = folder / "photo.HEIC"
        heic_path.write_bytes(b"heic image")

        collected = collect_supported_files(folder)
        plan = build_merge_plan([heic_path])

        assert collected == [heic_path]
        assert plan[0].source == heic_path
        assert plan[0].kind == "image"


def test_merge_files_to_pdf_converts_real_heic_image() -> None:
    from PIL import Image
    from pillow_heif import from_pillow

    with tempfile.TemporaryDirectory() as tmp_dir:
        base = Path(tmp_dir)
        heic_path = base / "photo.heic"
        from_pillow(Image.new("RGB", (20, 20), color="blue")).save(heic_path)
        out_path = base / "merged.pdf"

        result = merge_files_to_pdf([heic_path], out_path)

        assert result == out_path
        reader = PdfReader(str(out_path))
        assert len(reader.pages) == 1


def test_build_merge_plan_keeps_selected_order() -> None:
    with tempfile.TemporaryDirectory() as tmp_dir:
        base = Path(tmp_dir)

        pdf_a = base / "a.pdf"
        writer = __import__("pypdf").PdfWriter()
        writer.add_blank_page(width=100, height=100)
        with pdf_a.open("wb") as handle:
            writer.write(handle)

        image_b = base / "b.png"
        from PIL import Image

        Image.new("RGB", (20, 20), color="green").save(image_b)

        pdf_c = base / "c.pdf"
        writer = __import__("pypdf").PdfWriter()
        writer.add_blank_page(width=120, height=120)
        with pdf_c.open("wb") as handle:
            writer.write(handle)

        plan = build_merge_plan([pdf_a, image_b, pdf_c])

        assert [item.source for item in plan] == [pdf_a, image_b, pdf_c]
        assert all(item.kind in {"pdf", "image"} for item in plan)


def test_merge_files_to_pdf_creates_valid_output() -> None:
    with tempfile.TemporaryDirectory() as tmp_dir:
        base = Path(tmp_dir)

        pdf_path = base / "first.pdf"
        from pypdf import PdfWriter

        writer = PdfWriter()
        writer.add_blank_page(width=100, height=100)
        with pdf_path.open("wb") as handle:
            writer.write(handle)

        image_path = base / "second.png"
        from PIL import Image

        image = Image.new("RGB", (20, 20), color="blue")
        image.save(image_path)

        out_path = base / "merged.pdf"
        result = merge_files_to_pdf([pdf_path, image_path], out_path)

        assert result == out_path
        assert out_path.exists()
        reader = PdfReader(str(out_path))
        assert len(reader.pages) >= 2
