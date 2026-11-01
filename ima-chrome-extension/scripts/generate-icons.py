from pathlib import Path
import struct, zlib

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "icons"
OUT.mkdir(exist_ok=True)

def png_rgba(size):
    rows = []
    c = size // 2
    radius = max(2, int(size * 0.34))
    for y in range(size):
        row = bytearray([0])
        for x in range(size):
            dx, dy = x - c, y - c
            inside = dx*dx + dy*dy <= radius*radius
            # Simple IMA bridge mark: white central arch over transparent/dark field.
            r, g, b, a = (35, 35, 35, 255) if inside else (0, 0, 0, 0)
            if inside:
                if abs(dy) < max(1, size // 12) and abs(dx) < size // 3:
                    r = g = b = 255
                if abs(dx) < max(1, size // 14) and dy < 0:
                    r = g = b = 255
            row.extend((r, g, b, a))
        rows.append(bytes(row))

    raw = b"".join(rows)
    def chunk(kind, data):
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xffffffff)
    return (b"\x89PNG\r\n\x1a\n" +
            chunk(b"IHDR", struct.pack(">IIBBBBB", size, size, 8, 6, 0, 0, 0)) +
            chunk(b"IDAT", zlib.compress(raw, 9)) +
            chunk(b"IEND", b""))

for size in (16, 32, 48, 128):
    (OUT / f"icon{size}.png").write_bytes(png_rgba(size))
