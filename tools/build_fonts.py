# SPDX-License-Identifier: MIT
"""Development-only font bake. Pillow is not imported by the submitted renderer."""
import json
from pathlib import Path
import struct
import zlib
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
FONTS = Path('/usr/share/fonts/truetype/dejavu')
ROLES = {
    'mast': ('DejaVuSerif-Bold.ttf', 65),
    'lead': ('DejaVuSerif-Bold.ttf', 38),
    'side': ('DejaVuSerif-Bold.ttf', 31),
    'card': ('DejaVuSerif-Bold.ttf', 25),
    'bottom': ('DejaVuSerif-Bold.ttf', 27),
    'stat': ('DejaVuSans-Bold.ttf', 43),
    'body': ('DejaVuSans.ttf', 17),
    'small': ('DejaVuSans.ttf', 14),
    'label': ('DejaVuSans-Bold.ttf', 12),
    'deck': ('DejaVuSans.ttf', 19),
    'date': ('DejaVuSans-Bold.ttf', 17),
    'tiny': ('DejaVuSans.ttf', 11),
}

def main():
    index = {}
    pixels = bytearray()
    alphabet = ''.join(chr(i) for i in range(32, 127)) + '–—’“”·→↓€×'
    for role, (filename, size) in ROLES.items():
        font = ImageFont.truetype(str(FONTS / filename), size * 2)
        glyphs = {}
        for char in alphabet:
            left, top, right, bottom = font.getbbox(char, anchor='ls')
            w, h = right - left, bottom - top
            mask = Image.new('L', (max(1, w), max(1, h)))
            ImageDraw.Draw(mask).text((-left, -top), char, font=font,
                                      fill=255, anchor='ls')
            glyphs[char] = [font.getlength(char), left, top, w, h, len(pixels)]
            pixels.extend(mask.tobytes() if w and h else b'')
        index[role] = {'size': size, 'glyphs': glyphs}
    header = json.dumps(index, separators=(',', ':')).encode()
    payload = struct.pack('>I', len(header)) + header + pixels
    path = ROOT / 'assets' / 'type.pack'
    path.parent.mkdir(exist_ok=True)
    path.write_bytes(zlib.compress(payload, 9))
    print('Baked %s font roles: %s bytes' % (len(ROLES), path.stat().st_size))

if __name__ == '__main__':
    main()
