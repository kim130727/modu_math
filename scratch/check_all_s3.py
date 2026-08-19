import glob
import sys
from pathlib import Path

sys.path.insert(0, ".")
sys.path.insert(0, "tools")
from validate_generated_dsl import _run_build, _default_out_prefix

files = sorted(glob.glob("examples/problems/ko/S3_초등_3_*.dsl.py"))

failed = []

for f in files:
    dsl_path = Path(f)
    out_prefix = _default_out_prefix(dsl_path)
    try:
        _run_build(dsl_path=dsl_path, out_prefix=out_prefix, strict=False, emit_solvable=False)
    except Exception as e:
        failed.append((f, type(e).__name__, str(e)))

print(f"Total failures: {len(failed)}")
for f, err_type, err_msg in failed:
    print(f"{Path(f).name} | {err_type} | {err_msg}")
