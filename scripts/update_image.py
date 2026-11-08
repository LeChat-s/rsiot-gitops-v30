"""Set exactly one container image in the GitOps Deployment manifest."""
import re
import sys
from pathlib import Path

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python scripts/update_image.py ghcr.io/<owner>/rules:<sha>")
    image = sys.argv[1]
    if not re.fullmatch(r"ghcr\.io/[a-z0-9_.-]+/rules:[0-9a-f]{40}", image):
        raise SystemExit(f"invalid SHA-tagged GHCR image: {image}")
    file = Path(__file__).resolve().parent.parent / "infra" / "deployment.yaml"
    original = file.read_text(encoding="utf-8")
    updated, count = re.subn(r"(?m)^([ \t]*image:[ \t]*)ghcr\.io/[a-z0-9_.-]+/rules:[^\s]+[ \t]*$",
                             lambda match: match.group(1) + image,
                             original)
    if count != 1:
        raise SystemExit(f"expected exactly one image declaration; got {count}")
    file.write_text(updated, encoding="utf-8", newline="\n")
    print(f"Updated infra/deployment.yaml: {image}")
