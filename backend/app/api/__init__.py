from fastapi import APIRouter

from . import example_endpoints

router = APIRouter()

router.include_router(example_endpoints.router, prefix="/example", tags=["example"])
