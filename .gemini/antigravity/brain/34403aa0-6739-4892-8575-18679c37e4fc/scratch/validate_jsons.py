import json
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path("src").resolve()))

from modu_semantic_archive.schema import _validate_semantic_elements, SchemaValidationError
from modu_semantic_archive.contracts import canonicalize_semantic_json

def check_file(path):
    print(f"Checking {path}...")
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # 1. Basic structure check (manual based on schema.py logic)
        if "render" not in data or "canvas" not in data["render"] or "elements" not in data["render"]:
            print(f"  [FAIL] Missing render structure")
            return
            
        # 2. Element validation (internal logic)
        try:
            _validate_semantic_elements(data)
            print(f"  [OK] Elements are valid")
        except SchemaValidationError as e:
            print(f"  [FAIL] Element validation: {e}")
            
        # 3. Canonical order check
        # We can use the canonicalize_semantic_json function to see if it changes the order
        canonical = canonicalize_semantic_json(data)
        if list(data.keys()) != list(canonical.keys()):
            print(f"  [WARN] Root key order is not canonical")
            print(f"    Current: {list(data.keys())}")
            print(f"    Expected: {list(canonical.keys())}")
        else:
            print(f"  [OK] Root key order is canonical")

    except Exception as e:
        print(f"  [ERROR] {e}")

files = [
    "sample_data/problems/ke_3rd/0001/0001.semantic.json",
    "sample_data/problems/ke_3rd/0002/0002.semantic.json",
    "sample_data/problems/ke_3rd/0003/0003.semantic.json"
]

for f in files:
    check_file(f)
    print("-" * 20)
