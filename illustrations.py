# SPDX-License-Identifier: MIT
"""Original editorial spot illustrations drawn from geometric primitives."""
import math
from raster import INK, PAPER, MUTED, RED, TEAL, GOLD

PALE = (226, 231, 220)
ROSE = (237, 218, 203)

def tent(c, x, y, size: float=1, color=TEAL):
    c.polygon([(x,y),(x+32*size,y-30*size),(x+66*size,y)],color)
    c.polygon([(x+32*size,y-30*size),(x+43*size,y),(x+66*size,y)],INK)
    c.polygon([(x+25*size,y),(x+32*size,y-17*size),(x+39*size,y)],PAPER)
    c.line(x-6*size,y,x+72*size,y,INK,1.2)

def gaza(c, x, y, w=586, h=114):
    c.rect(x,y,w,h,ROSE)
    c.circle(x+w-66,y+34,23,(223,184,156))
    # A ruined urban silhouette, then temporary shelter and compromised water.
    for bx,bw,bh in [(15,38,50),(60,45,75),(113,30,58),(151,49,86),(207,24,48)]:
        c.polygon([(x+bx,y+93),(x+bx,y+93-bh),(x+bx+bw*.4,y+98-bh),
                   (x+bx+bw*.6,y+89-bh),(x+bx+bw,y+93-bh),(x+bx+bw,y+93)],MUTED)
        for wy in range(25, int(bh)-8, 17):
            c.rect(x+bx+9,y+93-wy,5,7,ROSE)
    c.rect(x,y+94,w,20,(216,195,172))
    tent(c,x+245,y+99,1.12)
    tent(c,x+337,y+104,.87)
    c.line(x+438,y+100,x+438,y+59,TEAL,5)
    c.line(x+438,y+60,x+459,y+60,TEAL,5)
    c.line(x+458,y+60,x+458,y+72,TEAL,5)
    c.polygon([(x+458,y+76),(x+452,y+87),(x+458,y+92),(x+464,y+87)],TEAL)
    c.circle(x+517,y+71,26,PAPER)
    c.rect(x+512,y+55,10,32,RED)
    c.rect(x+501,y+66,32,10,RED)
    c.line(x+9,y+h-1,x+w-9,y+h-1,INK,1)

def courthouse(c, x, y, w=290):
    c.rect(x,y,w,92,PALE)
    c.polygon([(x+29,y+29),(x+103,y+7),(x+177,y+29)],INK)
    c.rect(x+28,y+33,151,6,INK)
    for xx in (40,77,114,151):
        c.rect(x+xx,y+42,13,32,TEAL)
    c.rect(x+25,y+78,158,6,INK)
    c.rect(x+19,y+87,170,3,INK)
    c.rect(x+214,y+17,46,68,INK)
    c.rect(x+218,y+22,38,50,PAPER)
    for yy in (33,43,53):
        c.line(x+225,y+yy,x+249,y+yy,RED,3)
    c.circle(x+237,y+79,2,PAPER)

def ship(c, x, y):
    c.line(x,y+45,x+99,y+45,TEAL,1.5)
    c.line(x+7,y+51,x+114,y+51,TEAL,1.5)
    c.polygon([(x+5,y+23),(x+108,y+23),(x+91,y+39),(x+20,y+39)],INK)
    c.rect(x+38,y+10,28,13,MUTED)
    c.rect(x+53,y,2,17,INK)
    c.line(x+83,y+8,x+83,y+23,INK,2)
    c.line(x+77,y+12,x+90,y+12,INK,2)

def pulse(c, x, y):
    points=[(x,y+24),(x+18,y+24),(x+27,y+8),(x+38,y+44),
            (x+49,y+17),(x+60,y+24),(x+86,y+24)]
    for a,b in zip(points,points[1:]):c.line(*a,*b,RED,3)

def mine(c, x, y):
    c.polygon([(x+26,y),(x+52,y+45),(x,y+45)],GOLD)
    c.text('!',x+22,y+34,'bottom',INK)
    c.line(x-4,y+51,x+56,y+51,INK,1)

def chip(c, x, y):
    c.rect(x+9,y+9,42,42,TEAL)
    c.rect(x+16,y+16,28,28,PAPER)
    for i in range(4):
        q=16+i*9
        c.line(x+q,y+2,x+q,y+9,TEAL,2)
        c.line(x+q,y+51,x+q,y+58,TEAL,2)
        c.line(x+2,y+q,x+9,y+q,TEAL,2)
        c.line(x+51,y+q,x+58,y+q,TEAL,2)
    c.line(x+68,y+13,x+85,y+13,RED,3)
    c.line(x+85,y+13,x+85,y+43,RED,3)
    c.polygon([(x+78,y+38),(x+85,y+49),(x+92,y+38)],RED)

def trophy(c, x, y):
    c.circle(x+35,y+25,25,(232,218,180))
    c.polygon([(x+16,y+5),(x+54,y+5),(x+48,y+30),
               (x+35,y+38),(x+22,y+30)],GOLD)
    c.rect(x+32,y+35,6,17,INK)
    c.rect(x+21,y+52,28,5,INK)
    for side in (-1,1):
        a=x+35+side*20
        c.line(a,y+11,a+side*13,y+11,GOLD,4)
        c.line(a+side*13,y+11,a+side*9,y+28,GOLD,4)
        c.line(a+side*9,y+28,a-side*4,y+30,GOLD,4)

def globe(c, x, y, r=15):
    c.circle(x,y,r,TEAL)
    c.polygon([(x-r*.65,y-r*.4),(x-r*.2,y-r*.65),(x+r*.12,y-r*.2),
               (x-r*.2,y+r*.12),(x-r*.48,y)],PAPER)
    c.polygon([(x+r*.15,y+r*.1),(x+r*.6,y-r*.05),(x+r*.4,y+r*.6),
               (x+r*.1,y+r*.7)],PAPER)
