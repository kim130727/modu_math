import json
from pathlib import Path

def update_dsl(num, enriched_data):
    path = Path(f"sample_data/problems/ke_3rd/{num}/{num}.generated.py")
    if not path.exists():
        return
        
    # Read existing DSL
    content = path.read_text(encoding="utf-8")
    
    # We want to replace p.set_metadata(...) and p.set_domain(...)
    # with the enriched versions.
    # This is a bit tricky with string replacement, but I'll try to find the lines.
    
    metadata_json = json.dumps(enriched_data["metadata"], ensure_ascii=False, indent=4).replace("\n", "\n    ")
    domain_json = json.dumps(enriched_data["domain"], ensure_ascii=False, indent=4).replace("\n", "\n    ")
    
    # Simple replacement if they exist
    import re
    content = re.sub(r"p\.set_metadata\(.*?\)", f"p.set_metadata({metadata_json})", content, flags=re.DOTALL)
    content = re.sub(r"p\.set_domain\(.*?\)", f"p.set_domain({domain_json})", content, flags=re.DOTALL)
    
    path.write_text(content, encoding="utf-8")
    print(f"Updated DSL for {num}")

import json
for num in ["0001", "0002", "0003", "0004", "0005", "0006", "0007"]:
    json_path = Path(f"sample_data/problems/ke_3rd/{num}/{num}.semantic.json")
    if json_path.exists():
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        update_dsl(num, data)
