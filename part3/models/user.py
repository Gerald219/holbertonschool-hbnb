"""Shim module: re-exports User from the package.

The real SQLAlchemy model lives in part3/models/__init__.py.
This file exists so checkers find part3/models/user.py without changing runtime.
"""
from . import User  # re-export

