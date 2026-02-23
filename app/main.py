import logging

from fastapi import FastAPI

from app.api.v1.router import api_router
from app.config.policy import configurate_cors_policy
from app.core.logging import setup_logging
from app.config.context import lifespan

setup_logging()

logger = logging.getLogger(__name__)
app = FastAPI(
    title="Selectel Vacancies API",
    lifespan=lifespan
)
app.include_router(api_router)

configurate_cors_policy(app)
