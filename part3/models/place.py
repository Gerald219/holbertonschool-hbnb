"""Small shim: expose Place here.

The real SQLAlchemy model lives in part3/models/__init__.py.
This file exists so tools or checkers that expect part3/models/place.py
can import Place without changing how the app runs.
"""
from . import Place  # re-export

