#!/usr/bin/env python3
# -*- coding: encoding: utf-8 -*-
"""
HyperOS / Modern Qualcomm logo.img Pure Extractor
Copyright (C) 2026
Licensed under the MIT License.
"""

import argparse
import gzip
import os
import struct


def parse_and_extract(logo_path, output_dir):
    if not os.path.exists(logo_path):
        print(f"[-] Error: Input file '{logo_path}' does not exist.")
        return

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print("[*] Launching GZIP pure decompression matrix...")

    with open(logo_path, "rb") as f:
        # 1. 验证魔数
        f.seek(0x4000)
        header = f.read(8)
        if header != b"LOGO!!!!":
            print(
                "[-] Error: 'LOGO!!!!' magic number not found at 0x4000. Is this a valid modern logo image?"
            )
            return

        # 2. 读取图像块总数
        f.seek(0x400C)
        count = struct.unpack("<I", f.read(4))[0]
        if count == 0 or count > 100:
            count = 20  # 异常安全保护值
        print(f"[+] Detected embedded image entries: {count}")

        # 3. 解析 16 字节现代高通元数据索引表
        entries = []
        f.seek(0x4010)
        for i in range(count):
            entry_bytes = f.read(16)
            if len(entry_bytes) < 16:
                break

            # 提取相对偏移量与压缩流大小
            rel_offset, img_size = struct.unpack("<II", entry_bytes[:8])
            if img_size == 0:
                continue

            # 现代高通固件数据块的绝对基地址通常固定在 0x5000
            abs_offset = 0x5000 + rel_offset
            entries.append((i, abs_offset, img_size))

        # 4. 纯净流释放与解包
        extracted_count = 0
        for i, abs_offset, img_size in entries:
            f.seek(abs_offset)
            payload = f.read(img_size)

            # 握手 GZIP 核心魔数
            if payload.startswith(b"\x1f\x8b"):
                try:
                    # 直接解压原厂纯精肉数据，其内部已自带标准文件头
                    decompressed_data = gzip.decompress(payload)

                    # 自适应动态识别文件真实的拓展名
                    if decompressed_data.startswith(b"BM"):
                        ext = ".bmp"
                    elif decompressed_data.startswith(b"\x89PNG"):
                        ext = ".png"
                    else:
                        ext = ".bin"

                    out_name = f"logo_{i}{ext}"
                    out_path = os.path.join(output_dir, out_name)

                    with open(out_path, "wb") as out_f:
                        out_f.write(decompressed_data)

                    print(
                        f"  [+] Extracted: {out_name} ({len(decompressed_data)} bytes)"
                    )
                    extracted_count += 1
                except Exception as e:
                    print(f"  [-] Failed to decompress block {i}: {e}")

        print(
            f"\n[+] Success! Total {extracted_count} pristine images saved to '{output_dir}'"
        )


def main():
    parser = argparse.ArgumentParser(
        description="Extract raw PNG/BMP images from modern Qualcomm / Xiaomi HyperOS logo.img partitions seamlessly."
    )
    parser.add_argument(
        "-i",
        "--input",
        default="logo.img",
        help="Path to the input logo.img file (default: logo.img)",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="output_perfect",
        help="Path to the output directory (default: output_perfect)",
    )

    args = parser.parse_args()
    parse_and_extract(args.input, args.output)


if __name__ == "__main__":
    main()