"""Re-export from shared/confirmation — 保持向后兼容"""
import sys
import os

# 将 shared/ 加入 Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "shared"))

from confirmation import *  # noqa: F401,F403
from confirmation import __all__  # noqa: F401
