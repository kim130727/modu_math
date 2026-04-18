import shutil
import os
from pathlib import Path

root = Path(r"C:\projects\modu_math\sample_data\problems\ke_3rd")

for problem_dir in root.iterdir():
    if not problem_dir.is_dir():
        continue
    
    for sub in ["input", "output"]:
        sub_dir = problem_dir / sub
        if sub_dir.exists() and sub_dir.is_dir():
            print(f"Processing {sub_dir}")
            # Walk through sub_dir and move all files to problem_dir
            for dirpath, dirnames, filenames in os.walk(sub_dir):
                for filename in filenames:
                    src = Path(dirpath) / filename
                    dst = problem_dir / filename
                    
                    # If destination exists, we might want to handle it (e.g. overwrite or skip)
                    # For now, I'll overwrite to ensure we have the latest artifacts
                    if dst.exists():
                        print(f"  Overwriting {dst.name}")
                    
                    try:
                        shutil.move(str(src), str(dst))
                    except Exception as e:
                        print(f"  Error moving {filename}: {e}")
            
            # Remove the sub_dir
            try:
                shutil.rmtree(sub_dir)
                print(f"  Removed {sub_dir}")
            except Exception as e:
                print(f"  Error removing {sub_dir}: {e}")

print("Cleanup complete.")
