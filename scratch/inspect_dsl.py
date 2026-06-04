import glob
import re
import os

paths = sorted(glob.glob('examples/problems/TS_01.초등학교_3학년_01.객관식/S3_초등_3_00863[2-9]*.dsl.py') + glob.glob('examples/problems/TS_01.초등학교_3학년_01.객관식/S3_초등_3_00864[0-1]*.dsl.py'))
for path in paths:
    with open(path, encoding='utf-8') as f:
        content = f.read()
    slots = re.findall(r'TextSlot\(\s*id="([^"]+)"', content)
    regions_exp = re.search(r'id="region\.answer_explanation"[\s\S]*?slot_ids=\((.*?)\)', content)
    exp_slots = regions_exp.group(1).strip() if regions_exp else 'None'
    print(os.path.basename(path), 'Total slots:', len(slots), 'Explanation slot_ids:', exp_slots)
