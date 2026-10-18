# Offline PDF & Image Merger

This tool lets you select multiple PDF and image files, reorder them, and merge them into a single PDF without calling any external service.

## Features

- Select multiple files in one dialog
- Reorder files with simple up/down buttons
- Accepts PDFs and common image formats, including HEIC
- Converts HEIC images directly to PDF without creating an intermediate JPG
- Exports a single PDF file
- Works entirely on the local machine with no internet connection required at runtime
- No cloud upload or remote processing

## Security model

- All file processing stays on the local device.
- The program never uploads files to a remote server.
- No network calls are performed during selection, ordering, or export.
- The user controls the exact input and output paths.

## Run the app

From the project root:

```bash
python -m tool
```

## Dependencies

```bash
pip install pypdf Pillow pillow-heif
```

The HEIC decoder is provided by `pillow-heif`. During export, HEIC images are
opened locally, converted to RGB in memory, and added to the PDF; no JPG file
is created.

## Example usage

1. Click "Add files".
2. Select one or multiple PDF/image files.
3. Use the up/down buttons to define the final order.
4. Click "Merge to PDF" and choose the destination.
5. The output file is saved locally.
