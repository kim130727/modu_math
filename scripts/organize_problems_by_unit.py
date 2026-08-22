"""
Organizes problem files in examples/problems/ko into grade/semester/unit categorized folders.
"""
import os
import glob
import json
import shutil

def get_target_unit(base_name, sem_path):
    # 1. P3_1_01_... pattern
    if base_name.startswith('P3_1_01_'):
        return '3-1/1_덧셈과_뺄셈'
    if base_name.startswith('P3_1_02_'):
        return '3-1/2_평면도형'
    if base_name.startswith('P3_1_03_'):
        return '3-1/3_나눗셈'
    if base_name.startswith('P3_1_04_'):
        return '3-1/4_곱셈'
    if base_name.startswith('P3_1_05_'):
        return '3-1/5_길이와_시간'
    if base_name.startswith('P3_1_06_'):
        return '3-1/6_분수와_소수'
    if base_name.startswith('P3_2_01_'):
        return '3-2/1_곱셈'
    if base_name.startswith('P3_2_02_'):
        return '3-2/2_나눗셈'
    if base_name.startswith('P3_2_03_'):
        return '3-2/3_원'
    if base_name.startswith('P3_2_04_'):
        return '3-2/4_분수'
    if base_name.startswith('P3_2_05_'):
        return '3-2/5_들이와_무게'
    if base_name.startswith('P3_2_06_'):
        return '3-2/6_자료의_정리'

    # 2. Inspect semantic metadata
    if os.path.exists(sem_path):
        try:
            with open(sem_path, 'r', encoding='utf-8') as f:
                d = json.load(f)
                pt = str(d.get('problem_type', '')).lower()
                meta = d.get('metadata', {})
                title = str(meta.get('title', '')).lower()
                instr = str(meta.get('instruction', '')).lower()
                topic = str(meta.get('topic', '')).lower()
                tags = str(meta.get('tags', '')).lower()
                combined = f"{pt} {title} {instr} {topic} {tags}"

                if any(k in combined for k in ['원', 'circle', '지름', '반지름', '중심', '컴퍼스']):
                    return '3-2/3_원'
                if any(k in combined for k in ['들이', '무게', 'capacity', 'weight', '어림', '저울', '생수병', '물병', '리터', '밀리리터', '그램', '킬로그램']):
                    return '3-2/5_들이와_무게'
                if any(k in combined for k in ['곱셈', 'multiplication', 'product', '곱']):
                    return '3-1/4_곱셈'
                if any(k in combined for k in ['나눗셈', 'division', 'remainder', '몫', '나머지']):
                    return '3-1/3_나눗셈'
                if any(k in combined for k in ['평면도형', '직각', '삼각형', '직사각형', '정사각형', 'geometry', '도형']):
                    return '3-1/2_평면도형'
                if any(k in combined for k in ['분수', '소수', 'fraction']):
                    return '3-1/6_분수와_소수'
                if any(k in combined for k in ['길이', '시간', '거리', '시각', '초']):
                    return '3-1/5_길이와_시간'
                if any(k in combined for k in ['덧셈', '뺄셈', 'addition', 'subtraction', '세로셈', '받아올림', '수 모형']):
                    return '3-1/1_덧셈과_뺄셈'
        except Exception as e:
            print(f"Error reading {sem_path}: {e}")

    # Default fallback for S3_초등_3
    return '3-1/1_덧셈과_뺄셈'

def organize():
    ko_dir = r'c:\projects\modu_math\examples\problems\ko'
    renderers = glob.glob(os.path.join(ko_dir, '*.renderer.json'))
    print(f"Found {len(renderers)} problem sets in root {ko_dir}")

    counts = {}
    for r in renderers:
        filename = os.path.basename(r)
        base_name = filename[:-len('.renderer.json')]
        sem_path = os.path.join(ko_dir, f"{base_name}.semantic.json")
        target_sub = get_target_unit(base_name, sem_path)
        counts[target_sub] = counts.get(target_sub, 0) + 1

        target_dir = os.path.join(ko_dir, target_sub.replace('/', os.sep))
        os.makedirs(target_dir, exist_ok=True)

        # Move all matching files with prefix base_name
        pattern = os.path.join(ko_dir, f"{base_name}*")
        for f in glob.glob(pattern):
            if os.path.isfile(f):
                dst = os.path.join(target_dir, os.path.basename(f))
                shutil.move(f, dst)

    print("Organized problems count per unit:")
    for k, v in sorted(counts.items()):
        print(f"  {k}: {v} problems")

if __name__ == '__main__':
    organize()
