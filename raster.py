# SPDX-License-Identifier: MIT
"""Small deterministic RGB raster engine; Python standard library only."""
import json
import math
from pathlib import Path
import struct
import zlib

SCALE = 2
WIDTH = HEIGHT = 1024
PAPER = (246, 242, 232)
INK = (24, 40, 47)
MUTED = (85, 100, 104)
RED = (169, 57, 43)
TEAL = (28, 103, 108)
GOLD = (180, 135, 57)
RULE = (198, 201, 190)

class Canvas:
    def __init__(self):
        self.w = WIDTH * SCALE
        self.h = HEIGHT * SCALE
        self.pixels = bytearray(bytes(PAPER) * (self.w * self.h))
        data = zlib.decompress((Path(__file__).resolve().parent / 'assets/type.pack').read_bytes())
        n = struct.unpack_from('>I', data)[0]
        self.fonts = json.loads(data[4:4+n])
        self.masks = data[4+n:]
        self.boxes = []

    def rect(self, x, y, w, h, color):
        x0, y0 = max(0, round(x*SCALE)), max(0, round(y*SCALE))
        x1, y1 = min(self.w, round((x+w)*SCALE)), min(self.h, round((y+h)*SCALE))
        if x1 <= x0 or y1 <= y0: return
        row = bytes(color) * (x1-x0)
        for yy in range(y0, y1):
            start = (yy*self.w+x0)*3
            self.pixels[start:start+len(row)] = row

    def polygon(self, points, color):
        pts = [(x*SCALE, y*SCALE) for x, y in points]
        for y in range(max(0, math.floor(min(p[1] for p in pts))),
                       min(self.h, math.ceil(max(p[1] for p in pts)))):
            hits = []
            for (ax, ay), (bx, by) in zip(pts, pts[1:]+pts[:1]):
                if min(ay, by) <= y+0.5 < max(ay, by):
                    hits.append(ax+(y+0.5-ay)*(bx-ax)/(by-ay))
            hits.sort()
            for a, b in zip(hits[::2], hits[1::2]):
                lo, hi = max(0, math.ceil(a-0.5)), min(self.w, math.ceil(b-0.5))
                if hi > lo:
                    start = (y*self.w+lo)*3
                    self.pixels[start:start+(hi-lo)*3] = bytes(color)*(hi-lo)

    def line(self, x1, y1, x2, y2, color=INK, width: float=1):
        dx, dy = x2-x1, y2-y1
        length = math.hypot(dx, dy)
        if length == 0: return
        nx, ny = -dy/length*width/2, dx/length*width/2
        self.polygon([(x1+nx,y1+ny),(x2+nx,y2+ny),
                      (x2-nx,y2-ny),(x1-nx,y1-ny)], color)

    def circle(self, x, y, r, color):
        self.polygon([(x+math.cos(i*math.tau/64)*r,
                       y+math.sin(i*math.tau/64)*r) for i in range(64)], color)

    def measure(self, text, role='body', tracking=0):
        glyphs = self.fonts[role]['glyphs']
        return sum(glyphs[c][0]/SCALE for c in text) + max(0,len(text)-1)*tracking

    def text(self, text, x, baseline, role='body', color=INK, tracking=0):
        glyphs = self.fonts[role]['glyphs']
        start_x = x
        bounds = [float('inf'),float('inf'),float('-inf'),float('-inf')]
        for char in text:
            advance, left, top, w, h, offset = glyphs[char]
            xx, yy = round(x*SCALE)+left, round(baseline*SCALE)+top
            if w and h:
                bounds = [min(bounds[0],xx/SCALE),min(bounds[1],yy/SCALE),
                          max(bounds[2],(xx+w)/SCALE),max(bounds[3],(yy+h)/SCALE)]
            for v in range(h):
                if not 0 <= yy+v < self.h: continue
                for u in range(w):
                    if not 0 <= xx+u < self.w: continue
                    a = self.masks[offset+v*w+u]
                    if not a: continue
                    p = ((yy+v)*self.w+xx+u)*3
                    for channel in range(3):
                        old = self.pixels[p+channel]
                        self.pixels[p+channel] = (old*(255-a)+color[channel]*a+127)//255
            x += advance/SCALE+tracking
        self.boxes.append([text,*bounds,role])
        return x

    def wrap(self, text, x, baseline, width, role='body', color=INK, leading=24):
        lines = []
        for paragraph in text.split('\n'):
            line = ''
            for word in paragraph.split():
                proposed = (line+' '+word).strip()
                if line and self.measure(proposed,role) > width:
                    lines.append(line); line = word
                else: line = proposed
            lines.append(line)
        for i, line in enumerate(lines):
            if self.measure(line,role) > width: raise ValueError('Text too wide: '+line)
            self.text(line,x,baseline+i*leading,role,color)
        return baseline+(len(lines)-1)*leading

    def save(self, path):
        raw = bytearray()
        p = self.pixels
        stride = self.w*3
        for y in range(HEIGHT):
            raw.append(0)
            a = y*SCALE*stride
            for x in range(WIDTH):
                i = a+x*SCALE*3
                for c in range(3):
                    raw.append((p[i+c]+p[i+3+c]+p[i+stride+c]+p[i+stride+3+c]+2)//4)
        def chunk(name, payload):
            return struct.pack('>I',len(payload))+name+payload+struct.pack('>I',zlib.crc32(name+payload)&0xffffffff)
        header = struct.pack('>IIBBBBB',WIDTH,HEIGHT,8,2,0,0,0)
        output = b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',header)+chunk(b'IDAT',zlib.compress(raw,9))+chunk(b'IEND',b'')
        if len(output)>1048576: raise ValueError('Image exceeds 1 MiB')
        Path(path).write_bytes(output)
        return len(output)
