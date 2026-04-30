import os
import glob
import ast
import pprint

d1 = r'c:\projects\modu_math\examples\problems\260427'
files = glob.glob(os.path.join(d1, 'Hpdf_*.dsl.py'))

for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    if 'SOLVABLE = {' not in content: continue
    
    parts = content.split('SOLVABLE = ')
    pre_content = parts[0]
    solvable_str = parts[1]
    
    try:
        sol_dict = ast.literal_eval(solvable_str.strip())
        
        if 'plan' not in sol_dict:
            sol_dict['plan'] = ["풀이 과정 없음"]
                
        new_solvable_str = pprint.pformat(sol_dict, sort_dicts=False, width=100, indent=4)
        new_content = pre_content + 'SOLVABLE = ' + new_solvable_str + '\n'
        
        if new_content != content:
            with open(f, 'w', encoding='utf-8') as file:
                file.write(new_content)
            print(f"Fixed {os.path.basename(f)}")
    except Exception as e:
        pass
