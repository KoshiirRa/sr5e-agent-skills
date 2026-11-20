#!/usr/bin/env python3
"""
Root convenience wrapper for Shadowrun 5e Life Modules query and build validator utility.
"""
import importlib.util
import sys
from pathlib import Path

skill_script = (
    Path(__file__).resolve().parent.parent
    / ".agents"
    / "skills"
    / "sr5e-life-modules"
    / "scripts"
    / "life_modules.py"
)

if skill_script.exists():
    spec = importlib.util.spec_from_file_location("life_modules", skill_script)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.main()
else:
    print(f"Error: Could not locate life_modules.py at {skill_script}")
    sys.exit(1)
