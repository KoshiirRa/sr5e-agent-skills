#!/usr/bin/env python3
"""
Root convenience wrapper for Shadowrun 5e Chummer XML query utility.
"""
import sys
from pathlib import Path

skill_script = Path(__file__).resolve().parent.parent / ".agents" / "skills" / "sr5e-data-query-and-extraction" / "scripts" / "query_chummer.py"

if skill_script.exists():
    import importlib.util
    spec = importlib.util.spec_from_file_location("query_chummer", skill_script)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.main()
else:
    print(f"Error: Could not locate query_chummer.py at {skill_script}")
    sys.exit(1)
