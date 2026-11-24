# THE TUESDAY GLOBE — Tuesday 24 November 2026.
# Entry point: copies the finished front page to /output/entry.png.
# Standard library only: the grading sandbox installs nothing, so this
# program imports nothing beyond os, sys, shutil and pathlib. The image
# itself was drawn locally (see render.py, kept in this repo as the
# record of how it was made) and is shipped as entry.png beside this file.
import os
import shutil
import sys
from pathlib import Path

IMAGE_NAME = "entry.png"


def pick_destination(argv):
    """Decide where the finished page goes."""
    if len(argv) > 1:
        given = Path(argv[1])
        if given.is_dir():
            return given / IMAGE_NAME
        return given
    folder = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if folder:
        return Path(folder) / IMAGE_NAME
    return Path("/output") / IMAGE_NAME


def main(argv):
    here = Path(__file__).resolve().parent
    source = here / IMAGE_NAME
    if not source.is_file():
        print(f"missing shipped image: {source}", file=sys.stderr)
        return 1
    target = pick_destination(argv)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    size = target.stat().st_size
    if size != source.stat().st_size:
        print(f"copy incomplete: {target} [{size} bytes]", file=sys.stderr)
        return 1
    print(f"front page done -> {target} [{size} bytes]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
