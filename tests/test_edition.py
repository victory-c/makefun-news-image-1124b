# SPDX-License-Identifier: MIT
"""Standard-library tests for file integrity, determinism, and editorial layout."""
import hashlib
import json
import os
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
import unittest
import zlib

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
sys.dont_write_bytecode = True
from main import render
from raster import Canvas, INK, PAPER


def parse_png(data):
    assert data[:8] == b'\x89PNG\r\n\x1a\n'
    cursor, chunks = 8, []
    while cursor < len(data):
        n = struct.unpack_from('>I',data,cursor)[0]
        name = data[cursor+4:cursor+8]
        payload = data[cursor+8:cursor+8+n]
        crc = struct.unpack_from('>I',data,cursor+8+n)[0]
        assert zlib.crc32(name+payload)&0xffffffff == crc, 'Bad CRC'
        chunks.append((name,payload))
        cursor += n+12
    assert cursor == len(data)
    assert [c[0] for c in chunks] == [b'IHDR',b'IDAT',b'IEND']
    header = struct.unpack('>IIBBBBB',chunks[0][1])
    assert header == (1024,1024,8,2,0,0,0)
    raw = zlib.decompress(chunks[1][1])
    assert len(raw) == 1024*(1024*3+1)
    assert all(raw[i*(1024*3+1)] == 0 for i in range(1024))
    return raw


class EditionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.canvas = render()

    def test_text_inside_page(self):
        for text,x0,y0,x1,y1,role in self.canvas.boxes:
            self.assertGreaterEqual(x0,30,text)
            self.assertGreaterEqual(y0,18,text)
            self.assertLessEqual(x1,995,text)
            self.assertLessEqual(y1,1005,text)

    def test_text_does_not_overlap(self):
        boxes = self.canvas.boxes
        for i,a in enumerate(boxes):
            for b in boxes[i+1:]:
                overlap = min(a[3],b[3])-max(a[1],b[1]) > .5 and min(a[4],b[4])-max(a[2],b[2]) > .5
                self.assertFalse(overlap,(a[0],b[0]))

    def test_seven_stories_and_date(self):
        text = '\n'.join(b[0] for b in self.canvas.boxes)
        for phrase in ['TUESDAY 24 NOVEMBER 2026','Gaza:','Huawei','Italy warns',
                       'Health gains','Landmine toll','Nvidia scrutiny','Senegal restored']:
            self.assertIn(phrase,text)
        self.assertIn('cases in October.',text)
        self.assertIn('2025 Africa Cup',text)
        self.assertIn('weekend strikes',text)

    def test_font_data_complete(self):
        for role, font in self.canvas.fonts.items():
            for char, spec in font['glyphs'].items():
                advance,left,top,w,h,offset = spec
                self.assertGreaterEqual(advance,0,(role,char))
                self.assertLessEqual(offset+w*h,len(self.canvas.masks),(role,char))
        with self.assertRaises(KeyError):
            self.canvas.measure('unsupported: \u2603')

    def test_guarded_wrap(self):
        with self.assertRaises(ValueError):
            self.canvas.wrap('Unbreakable',0,0,1)

    def test_png_integrity_and_repeat_bytes(self):
        with tempfile.TemporaryDirectory(prefix='news-test-',dir=os.environ.get('TMPDIR')) as tmp:
            a,b = Path(tmp)/'a.png',Path(tmp)/'b.png'
            self.canvas.save(a);self.canvas.save(b)
            data=a.read_bytes()
            self.assertEqual(data,b.read_bytes())
            self.assertLessEqual(len(data),1048576)
            parse_png(data)
            print('PNG sha256:',hashlib.sha256(data).hexdigest())

    def test_entrypoint_foreign_cwd_clean_env(self):
        with tempfile.TemporaryDirectory(prefix='news-run-',dir=os.environ.get('TMPDIR')) as tmp:
            outputs = []
            for i in range(2):
                out=Path(tmp)/('output with spaces %s' % i)
                result=subprocess.run([sys.executable,'-P','-s',str(ROOT/'main.py')],
                    cwd='/',env={'MAKEFUN_OUTPUT_DIR':str(out),'PYTHONHASHSEED':str(i)},
                    timeout=30,capture_output=True,text=True,check=True)
                self.assertEqual(sorted(p.name for p in out.iterdir()),['entry.png'])
                self.assertIn('1024 x 1024',result.stdout)
                self.assertEqual(result.stderr,'')
                outputs.append((out/'entry.png').read_bytes())
            self.assertEqual(outputs[0],outputs[1])

if __name__ == '__main__':
    unittest.main(verbosity=2)
