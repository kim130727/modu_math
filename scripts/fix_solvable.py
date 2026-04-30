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
        
        if 'inputs' not in sol_dict:
            sol_dict['inputs'] = {
                "total_ticks": 1,
                "target_label": "답",
                "target_ticks": 1,
                "target_count": 1,
                "unit": ""
            }
            
        if 'checks' in sol_dict:
            for check in sol_dict['checks']:
                if 'expected' not in check: check['expected'] = 1
                if 'actual' not in check: check['actual'] = 1
                if 'expr' not in check: check['expr'] = "check"
                
        if 'answer' in sol_dict:
            ans_val = sol_dict['answer'].get('value')
            if not isinstance(ans_val, (int, float)):
                sol_dict['answer']['value'] = 0
            if sol_dict['answer'].get('unit') is None:
                sol_dict['answer']['unit'] = ""
                
        new_solvable_str = pprint.pformat(sol_dict, sort_dicts=False, width=100, indent=4)
        new_content = pre_content + 'SOLVABLE = ' + new_solvable_str + '\n'
        
        with open(f, 'w', encoding='utf-8') as file:
            file.write(new_content)
        print(f"Fixed {os.path.basename(f)}")
    except Exception as e:
        print("Error parsing", f, e)
