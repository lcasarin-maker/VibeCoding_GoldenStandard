import sys

# Windows consoles default to cp1252; catalog text is UTF-8 (arrows, accents).
for stream in (sys.stdout, sys.stderr):
    if stream.encoding != "utf-8" and hasattr(stream, "reconfigure"):
        stream.reconfigure(encoding="utf-8")

from gs_query.cli import main

if __name__ == "__main__":
    sys.exit(main())
