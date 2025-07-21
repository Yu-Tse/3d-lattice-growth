# src/__init__.py
"""
CUDA‑FCC Growth Simulator
=========================
Convenience imports for quick access.
"""
from .simulation import run_sim  # 常用 API

__all__ = ["run_sim"]
__version__ = "0.1.0"