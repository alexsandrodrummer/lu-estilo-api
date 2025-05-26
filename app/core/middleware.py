from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
import logging

def add_exception_handler(app: FastAPI):

    @app.middleware("http")
    async def catch_exceptions_middleware(request: Request, call_next):
        try:
            return await call_next(request)
        except Exception as e:
            logging.error(f"Erro não tratado: {e}")
            return JSONResponse(
                status_code=500,
                content={"detail": "Erro interno do servidor"}
            )
