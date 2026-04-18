import json
from pathlib import Path

root = Path(r"C:\projects\modu_math\sample_data\problems\korea_elementary")

results = []
for p_dir in root.iterdir():
    if not p_dir.is_dir(): continue
    
    # Try to find semantic.json in output/json or input/json or directly
    s_paths = [
        p_dir / "output" / "json" / f"{p_dir.name}.semantic.json",
        p_dir / "input" / "json" / f"{p_dir.name}.semantic.json",
        p_dir / f"{p_dir.name}.semantic.json"
    ]
    
    found = False
    for s_path in s_paths:
        if s_path.exists():
            with open(s_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            title = data.get("title", "")
            p_type = data.get("problem_type", "")
            instr = ""
            # Try to get instruction from domain or render
            if "domain" in data and "instruction" in data["domain"]:
                instr = data["domain"]["instruction"]
            elif "render" in data and "elements" in data["render"]:
                for el in data["render"]["elements"]:
                    if el.get("id") == "instruction" or el.get("semantic_role") == "instruction":
                        instr = el.get("text", "")
                        break
            
            results.append({
                "id": p_dir.name,
                "title": title,
                "type": p_type,
                "instruction": instr
            })
            found = True
            break
    if not found:
        results.append({"id": p_dir.name, "error": "Not found"})

for res in results:
    print(res)
