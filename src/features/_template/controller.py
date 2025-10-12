""" Router module template for feature endpoints

This file defines a FastAPI APIRouter instance that handles
all routes prefixed with a chosen prefix.

Each route function under this router is responsible for specific
template-related operations (e.g., fetching, creating, or updating templates).

The router is designed to be imported and included in the
__init__.py file.

Example:
  from .controller import router as template_router
"""

from fastapi import APIRouter

router = APIRouter(
      prefix="/example"
)

@router.get("/")
def function_name():
    ...
