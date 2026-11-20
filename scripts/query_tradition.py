#!/usr/bin/env python3
"""
Root convenience wrapper for Shadowrun 5e traditions query utility.
"""
import sys
from pathlib import Path

skill_script = Path(__file__).resolve().parent.parent / ".agents" / "skills" / "sr5e-traditions" / "scripts" / "query_tradition.py"

if skill_script.exists():
    import importlib.util
    spec = importlib.util.spec_from_file_location("query_tradition", skill_script)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.main()
else:
    print(f"Error: Could not locate query_tradition.py at {skill_script}")
    sys.exit(1)
