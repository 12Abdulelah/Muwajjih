from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from muwajjih.adapters.model.sklearn import SklearnDepartmentModel
from muwajjih.adapters.supabase.client import create_supabase_client
from muwajjih.adapters.supabase.repo import SupabasePredictionRepository
from muwajjih.api.errors import unhandled_exception_handler, validation_exception_handler
from muwajjih.api.trace import TraceIdMiddleware
from muwajjih.api.routes import router
from muwajjih.config import Settings
from muwajjih.logs import configure_logging
from muwajjih.service.triage import TriageService


def create_app(service_override: TriageService | None = None) -> FastAPI:
    settings = Settings()
    configure_logging(settings.log_level)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        app.state.ready = False
        if service_override is not None:
            app.state.triage_service = service_override
            app.state.ready = True
            yield
            app.state.ready = False
            return

        model = SklearnDepartmentModel(settings.model_path)
        model.load()
        model.warm_up()
        repository = None
        if settings.supabase_url and settings.supabase_key:
            client = create_supabase_client(settings.supabase_url, settings.supabase_key)
            repository = SupabasePredictionRepository(client)
        app.state.model = model
        app.state.triage_service = TriageService(model=model, repository=repository)
        app.state.ready = True
        yield
        app.state.ready = False

    app = FastAPI(title="Muwajjih", version="1.0.0", lifespan=lifespan)
    app.add_middleware(TraceIdMiddleware)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)
    app.include_router(router)
    return app


app = create_app()
