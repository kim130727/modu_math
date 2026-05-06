import os
import re

root_dir = r"C:\projects\modu_math\examples\problems\korea_elementary"

fixed_count = 0
for root, dirs, files in os.walk(root_dir):
    parent_dir_name = os.path.basename(root)
    expected_dsl = f"{parent_dir_name}.dsl.py"
    
    if expected_dsl in files:
        path = os.path.join(root, expected_dsl)
        
        try:
            # Read as bytes first to handle potential encoding issues caused by the corruption
            with open(path, 'rb') as f:
                raw_content = f.read()
            
            # Try to decode, replacing errors
            content = raw_content.decode('utf-8', errors='replace')
            
            # The pattern should be robust enough to find the id assignment in ProblemTemplate
            # We want to replace everything from 'id=' to the next comma or closing paren
            pattern = re.compile(r"(ProblemTemplate\s*\(\s*)id\s*=\s*.*?(,\s*title)", re.DOTALL)
            replacement = rf"\1id='{parent_dir_name}'\2"
            
            new_content = pattern.sub(replacement, content)
            
            if new_content != content or b'\x80' in raw_content:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Fixed: {path}")
                fixed_count += 1
        except Exception as e:
            print(f"Error fixing {path}: {e}")

print(f"Total files fixed: {fixed_count}")
