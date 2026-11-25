# Validation record

The image was rendered in three layout iterations during the recorded build.
No scoring result is claimed: RULES.txt explicitly says this competition has no
local grader. Pairwise judging and transcript checks happen on the server.

## Verified locally

- Python standard-library test suite: seven tests passed.
- Complete 1024×1024 RGB PNG: every chunk CRC and decompressed row verified.
- Final image: 128,318 bytes, below the 1,048,576-byte limit.
- SHA-256: `7af747440cbb8ab650824fd72368f7892a73cec9b6d85baddfaaf0d4594fcdde`.
- Seven labeled stories, explicit Tuesday 24 November 2026 date.
- Actual glyph bounds stay on the page; no text boxes overlap.
- Repeated runs and different Python hash seeds produce identical bytes.
- Clean-environment execution from `/`, including an output path with spaces.
- Headless Chromium decodes the PNG at native 1024×1024, with no page errors.
- Native-size and 512-pixel browser screenshots were captured locally.
- Tesseract recovers all seven stories at native size; thumbnail OCR recovers
  headlines but does not reliably recover every caption.

## Restrictive server simulation

`tools/sandbox_check.py` extracts a committed snapshot to a separate read-only
copy and runs the exact entrypoint twice inside the available Python 3.13.17
container image. The command uses:

- `python3 -P -s /bot/main.py`, working directory `/`.
- `env -i` with only `MAKEFUN_OUTPUT_DIR=/output`.
- UID/GID 65534; read-only `/bot` and read-only root filesystem.
- No network, no capabilities, no privilege escalation.
- 512 MiB memory, no swap, one CPU, 64 processes.
- An outer 30-second timeout, stricter than the contest's 60-second limit.

Both stage-three sandbox runs exited 0 with empty stderr, taking 5.758 and
5.666 seconds including container startup. Each produced only `entry.png`, owned
by UID 65534, with the hash above. The final handoff repeats this on final HEAD.

## Kit check and remaining gate

The supplied level-39 kit and separately downloaded current level-46 kit both
pass competition-open, snapshot size, MIT SPDX license, and Python entrypoint
checks. With no transcript argument they both fail only `transcripts_present`.
This is not suppressed or described as a full check pass. The user explicitly
reserved bundling and submission for the wrapper after the session ends. That
wrapper must bundle the real recorded session and re-run the transcript gate.
No transcript was fabricated, exported from memory, edited, or bundled here.

The session provides no image-viewing/vision tool. Browser and OCR checks were
performed, but no human or vision-model visual inspection is claimed. Source
facts were checked against fetched reporting; selection remains an editorial
judgment, not a certified exhaustive news digest.
