# HyperOS Logo Extractor

A lightweight, zero-dependency Python script to seamlessly extract pristine BMP/PNG splash images from modern Xiaomi (HyperOS) and Qualcomm `logo.img` partitions.

## Features
- **Zero Dependencies**: Powered entirely by Python standard libraries (`gzip`, `struct`).
- **Modern Layout Support**: Perfectly parses the modern 16-byte Qualcomm index table.
- **Auto Decompression**: Automatically detects and inflates embedded GZIP streams (`1F 8B`).

## Usage
Put your `logo.img` in the same directory and run:
```bash
python hyperos-logo-extractor.py -i logo.img -o output_perfect
