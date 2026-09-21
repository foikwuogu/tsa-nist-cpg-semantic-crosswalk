"""Append a fetch record to data/raw/PROVENANCE.txt.

Usage: python3 provenance.py <filepath> <source_url> <access_date> <license> <method>
"""
import hashlib
import os
import sys
from datetime import datetime, timezone

PROV_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "raw", "PROVENANCE.txt")


def record(filepath, source_url, access_date, license_str, method):
    with open(filepath, "rb") as f:
        content = f.read()
    sha256 = hashlib.sha256(content).hexdigest()
    line = (
        f"{os.path.basename(filepath)} | bytes={len(content)} | sha256={sha256} | "
        f"source={source_url} | accessed={access_date} | license={license_str} | "
        f"method={method} | logged={datetime.now(timezone.utc).isoformat()}\n"
    )
    os.makedirs(os.path.dirname(PROV_PATH), exist_ok=True)
    with open(PROV_PATH, "a") as f:
        f.write(line)
    print(line.strip())


if __name__ == "__main__":
    record(*sys.argv[1:6])
