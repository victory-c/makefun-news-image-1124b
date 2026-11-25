# SPDX-License-Identifier: MIT
"""24 November 2026: a researched, offline, deterministic world front page."""
import json
import os
from pathlib import Path
import sys

# The grader uses -P, runs with cwd elsewhere, and mounts the repository read-only.
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from raster import Canvas, INK, PAPER, MUTED, RED, TEAL, GOLD, RULE
from illustrations import gaza, courthouse, ship, pulse, mine, chip, trophy, globe


def label(c, text, x, y, color=TEAL):
    c.text(text,x,y,'label',color,1.3)


def render():
    c = Canvas()
    c.rect(0,0,1024,9,INK)
    label(c,'ONE DAY. SEVEN STORIES. A WORLD IN VIEW.',36,34)
    globe(c,970,29,12)
    c.text('THE WORLD TODAY',32,104,'mast')
    c.line(889,52,889,106,RULE,1)
    c.text('24',911,88,'stat',RED)
    label(c,'NOV 2026',908,107)
    c.line(36,121,988,121,INK,2)
    c.text('TUESDAY 24 NOVEMBER 2026',36,147,'date')
    c.text('GLOBAL EDITION  /  24.11.26',700,146,'small',MUTED)
    c.line(36,159,988,159,INK,.7)
    c.text('Conflict, health and technology reshape the day',36,190,'deck',MUTED)
    c.line(36,208,988,208,RULE,.8)

    label(c,'01 / MIDDLE EAST',36,233,RED)
    c.text('Gaza: strikes and',34,277,'lead')
    c.text('a disease alarm',34,321,'lead')
    gaza(c,36,341,580,114)
    c.wrap('Israeli strikes kill at least seven, including Hamas security chief '
           'Naeem Abu Nahel, officials say. Gaza issues a meningitis alert: '
           '272 cases in October.',36,482,580,'body',leading=24)
    c.text('BBC; THE GUARDIAN  /  REPORTED 24 NOV',36,562,'tiny',MUTED)

    c.line(638,225,638,566,RULE,.8)
    label(c,'02 / US–CHINA',660,233)
    c.text('Huawei guilty',658,275,'side')
    c.text('on 10 counts',658,312,'side')
    courthouse(c,660,341,328)
    c.wrap('US jury convicts the tech giant of trade-secrets conspiracy and '
           'bank fraud, but acquits it of racketeering.',660,460,328,'body',leading=24)
    c.text('BBC; AL JAZEERA  /  24 NOV',660,562,'tiny',MUTED)

    c.line(36,582,988,582,INK,1.5)
    label(c,'03 / EUROPE + NORTH AFRICA',36,607)
    c.text('Italy warns of',35,643,'card')
    c.text('war’s wider reach',35,674,'card')
    ship(c,39,691)
    c.wrap('Rome warns against escalation after Ukraine’s weekend strikes '
           'on Russian ships off Libya.',36,768,298,'body',leading=23)
    c.text('THE GUARDIAN  /  24 NOV',36,869,'tiny',MUTED)

    c.line(350,601,350,872,RULE,.8)
    label(c,'04 / CUBA',372,607)
    c.text('Health gains',371,643,'card')
    c.text('in reverse',371,674,'card')
    c.text('74.4',371,730,'stat',RED)
    c.text('YEARS',498,728,'label',MUTED)
    pulse(c,566,693)
    c.wrap('WHO chief says life expectancy fell from 78.8 in 2020 to 74.4 in '
           '2025, amid a severe economic crisis.',372,768,287,'body',leading=23)
    c.text('AFP / THE GUARDIAN  /  24 NOV',372,869,'tiny',MUTED)

    c.line(677,601,677,872,RULE,.8)
    label(c,'05 / GLOBAL SAFETY',699,607)
    c.text('Landmine toll',698,643,'card')
    c.text('at five-year high',698,674,'card')
    c.text('6,929',698,730,'stat',RED)
    mine(c,922,689)
    c.wrap('Mine and war-remnant victims in 2025, says today’s report. Myanmar '
           'and Syria lead; 84% were civilians.',699,768,289,'body',leading=23)
    c.text('LANDMINE MONITOR / AJ  /  24 NOV',699,869,'tiny',MUTED)

    c.line(36,888,988,888,INK,1.5)
    label(c,'06 / BUSINESS',36,913)
    c.text('BBC',470,913,'tiny',MUTED)
    chip(c,36,927)
    c.text('Nvidia scrutiny',146,949,'bottom')
    c.wrap('US attorney general declines to confirm a Huang probe. Shares '
           'close down nearly 6%.',146,975,350,'small',leading=19)
    c.line(519,906,519,1000,RULE,.8)
    label(c,'07 / AFRICAN SPORT',541,913)
    c.text('BBC SPORT',922,913,'tiny',MUTED)
    trophy(c,541,930)
    c.text('Senegal restored',629,949,'bottom')
    c.wrap('Sports court reinstates Senegal as 2025 Africa Cup of Nations '
           'champions.',629,975,359,'small',leading=19)
    return c


def main():
    directory = Path(os.environ.get('MAKEFUN_OUTPUT_DIR','/output'))
    directory.mkdir(parents=True,exist_ok=True)
    c = render()
    size = c.save(directory/'entry.png')
    if os.environ.get('MAKEFUN_DEBUG') == '1':
        (directory/'layout.json').write_text(json.dumps(c.boxes,indent=2))
    print('entry.png: 1024 x 1024; %s bytes' % size)

if __name__ == '__main__':
    main()
