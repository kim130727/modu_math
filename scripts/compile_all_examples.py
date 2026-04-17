import sys
from pathlib import Path
import importlib.util
import traceback

def compile_file(filepath: Path) -> bool:
    try:
        # Load the module dynamically
        spec = importlib.util.spec_from_file_location("problem_module", filepath)
        if spec is None or spec.loader is None:
            return False
        
        module = importlib.util.module_from_spec(spec)
        sys.modules["problem_module"] = module
        spec.loader.exec_module(module)
        
        if hasattr(module, "build"):
            problem = module.build()
            out_prefix = filepath.parent / filepath.name.replace(".generated.py", "")
            problem.save(out_prefix)
            return True
        return False
    except Exception as e:
        print(f"Error compiling {filepath}: {e}")
        traceback.print_exc()
        return False
    finally:
        if "problem_module" in sys.modules:
            del sys.modules["problem_module"]

def main():
    root = Path("c:/projects/modu_math/examples/problem")
    generated_files = list(root.rglob("*.generated.py"))
    
    # We will just compile the first 500 to verify it works
    to_compile = generated_files[:500]
    print(f"Found {len(generated_files)} generated files. Compiling {len(to_compile)} for test...")
    
    success = 0
    failed = 0
    
    for f in to_compile:
        if compile_file(f):
            success += 1
        else:
            failed += 1
            
    print(f"Results: {success} succeeded, {failed} failed.")

if __name__ == "__main__":
    main()
