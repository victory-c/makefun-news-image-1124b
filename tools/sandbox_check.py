# SPDX-License-Identifier: MIT
"""Exercise a committed snapshot under the server's restrictive runtime contract."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import subprocess
import tarfile
import time


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out',required=True)
    parser.add_argument('--image',default='d98cc29d3266')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    out = Path(args.out).resolve()
    out.mkdir(parents=True,exist_ok=False)
    bot = out/'bot'
    bot.mkdir()
    archive = subprocess.check_output(['git','archive','HEAD'],cwd=root)
    with tarfile.open(fileobj=io.BytesIO(archive)) as tar:
        tar.extractall(bot,filter='data')
    for item in bot.rglob('*'):
        item.chmod(0o555 if item.is_dir() else 0o444)
    bot.chmod(0o555)
    commit = subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()
    results = []
    command = []
    for i in range(2):
        target = out/('run-%s' % (i+1))
        target.mkdir(mode=0o777)
        target.chmod(0o777)
        command = ['timeout','30s','sudo','-n','docker','run','--rm',
            '--network','none','--read-only','--user','65534:65534',
            '--memory','512m','--memory-swap','512m','--cpus','1',
            '--pids-limit','64','--cap-drop','ALL',
            '--security-opt','no-new-privileges','--workdir','/',
            '--mount','type=bind,source=%s,target=/bot,readonly' % bot,
            '--mount','type=bind,source=%s,target=/output' % target,
            args.image,'/usr/bin/env','-i','MAKEFUN_OUTPUT_DIR=/output',
            '/usr/local/bin/python3','-P','-s','/bot/main.py']
        start = time.monotonic()
        process = subprocess.run(command,capture_output=True,text=True,timeout=40)
        elapsed = time.monotonic()-start
        if process.returncode:
            raise RuntimeError('Sandbox failed: '+process.stdout+process.stderr)
        files = sorted(p.name for p in target.iterdir())
        assert files == ['entry.png'],files
        png = target/'entry.png'
        data = png.read_bytes()
        assert data[:8] == b'\x89PNG\r\n\x1a\n'
        assert png.stat().st_uid == 65534
        assert len(data) <= 1048576
        results.append({'run':i+1,'exit_code':process.returncode,
            'wall_seconds_including_container_startup':round(elapsed,3),
            'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),
            'output_uid':png.stat().st_uid,'files':files,
            'stdout':process.stdout.strip(),'stderr':process.stderr})
    assert results[0]['sha256'] == results[1]['sha256']
    result = {'commit':commit,'python_image':args.image,
        'command':command,'runtime_contract':{
            'cwd':'/','uid':65534,'network':'none','repository':'read-only copy at /bot',
            'root_filesystem':'read-only','environment':'env -i; MAKEFUN_OUTPUT_DIR only',
            'memory_mb':512,'cpus':1,'pids':64,'outer_timeout_seconds':30,
            'entrypoint':'python3 -P -s /bot/main.py'},'runs':results,'identical':True}
    (out/'sandbox-result.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))

if __name__ == '__main__':
    main()
