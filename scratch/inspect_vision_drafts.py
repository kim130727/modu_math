import glob
import os
import re

paths = sorted(glob.glob('examples/problems/TS_01.초등학교_3학년_01.객관식/S3_초등_3_00863[2-9]*.vision_draft.md') + glob.glob('examples/problems/TS_01.초등학교_3학년_01.객관식/S3_초등_3_00864[0-1]*.vision_draft.md'))
for path in paths:
    print('========================================')
    print(os.path.basename(path))
    print('========================================')
    with open(path, encoding='utf-8') as f:
        content = f.read()
    
    # Extract the [보이는 텍스트] section
    match = re.search(r'\[보이는 텍스트\]([\s\S]*?)\[', content)
    if not match:
        # try to extract until the end or next heading
        match = re.search(r'\[보이는 텍스트\]([\s\S]*)', content)
        
    if match:
        print(match.group(1).strip())
    else:
        print("Not found")
