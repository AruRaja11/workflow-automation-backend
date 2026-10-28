import logging 
from core.logging_cofig import setup_logging
from api.routes.health import router as health_router 
from api.routes.outreach import router as outreach_router
from api.routes.previous_runs import router as previous_run_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from middleware.request_logging import (
    request_logging_middleware,
)

def create_app() -> FastAPI:
    setup_logging()

    
    app = FastAPI(
        description="client outreach automation",
        version='1.0.0',
        title="client outreach automation"
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["https://localhost:3000"],
        allow_credentials=False,
        allow_methods=["GET", "POST"],
        allow_headers=["Content-Type", "Authorization"]
    )

    app.middleware("http")(request_logging_middleware)

    app.include_router(
        outreach_router,
        prefix="/app/v1",
    )

    app.include_router(
        health_router,
        prefix="/app/v1",
    )

    app.include_router(
        previous_run_router,
        prefix="/app/v1"
    )
    return app 


app = create_app()
