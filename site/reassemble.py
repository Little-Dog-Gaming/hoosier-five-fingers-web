"""Rebuild the web export from chunks (run by CI, root of the site tree)."""
import hashlib, json, os, sys

manifest = json.load(open("manifest.json", encoding="utf-8"))
failed = 0
for entry in manifest["files"]:
    target = entry["path"]
    if entry["chunks"]:
        with open(target, "wb") as out:
            for name in entry["chunks"]:
                with open(name, "rb") as part:
                    while True:
                        block = part.read(1 << 22)
                        if not block:
                            break
                        out.write(block)
        for name in entry["chunks"]:
            os.remove(name)
    digest = hashlib.sha256(open(target, "rb").read()).hexdigest()
    ok = digest.upper() == entry["sha256"].upper()
    print(("OK   " if ok else "FAIL ") + target + " " + digest[:16])
    failed += 0 if ok else 1
print("reassembly failures: %d" % failed)
sys.exit(1 if failed else 0)
