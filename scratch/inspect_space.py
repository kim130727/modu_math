import glob
import re
import os

paths = sorted(glob.glob('examples/problems/TS_01.초등학교_3학년_01.객관식/S3_초등_3_00863[2-9]*.dsl.py') + glob.glob('examples/problems/TS_01.초등학교_3학년_01.객관식/S3_초등_3_00864[0-1]*.dsl.py'))
for path in paths:
    with open(path, encoding='utf-8') as f:
        content = f.read()
    
    w_match = re.search(r'width=(\d+)', content)
    h_match = re.search(r'height=(\d+)', content)
    w = w_match.group(1) if w_match else '?'
    h = h_match.group(1) if h_match else '?'
        
    # Find all y-coordinates
    ys = [float(y) for y in re.findall(r'y\s*=\s*([\d\.]+)', content)]
    y1s = [float(y) for y in re.findall(r'y1\s*=\s*([\d\.]+)', content)]
    y2s = [float(y) for y in re.findall(r'y2\s*=\s*([\d\.]+)', content)]
    all_ys = ys + y1s + y2s
    max_y = max(all_ys) if all_ys else 0
    
    print(os.path.basename(path), f"Canvas: {w}x{h}", "Max slot Y:", max_y)
