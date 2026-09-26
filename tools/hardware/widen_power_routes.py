#!/usr/bin/env python3
"""Compatibility entry point for continuous, standard-width power routing."""
from pathlib import Path
import runpy
runpy.run_path(str(Path(__file__).with_name('normalize_power_widths.py')),run_name='__main__')
