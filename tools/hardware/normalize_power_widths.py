#!/usr/bin/env python3
"""Compatibility entry point for guarded, whole-run width normalization.

The old per-segment optimizer retained wide islands and arbitrary steps. Use
read-only geometric triage plus transactional whole-run widening instead.
Placement changes and route reconstruction remain explicit engineering edits.
Requires the hardware environment with pcbnew and Shapely 2.
"""
from pathlib import Path
import subprocess,sys
root=Path(__file__).resolve().parents[2]
subprocess.run([sys.executable,str(Path(__file__).with_name('apply_width_triage.py'))],cwd=root,check=True)
