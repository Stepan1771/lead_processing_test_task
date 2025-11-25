from fastapi import APIRouter

from core.config import settings

from .contacts import router as contact_router
from .leads import router as lead_router
from .operators import router as operator_router
from .sources import router as source_router




router = APIRouter(
    prefix=settings.api.v1.prefix,
)

router.include_router(contact_router)
router.include_router(lead_router)
router.include_router(operator_router)
router.include_router(source_router)