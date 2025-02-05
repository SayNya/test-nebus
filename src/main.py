from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from src.config import settings
from src.infrastructure import application
from src.infrastructure.database.session import sessionmanager
from src.presentation import rest


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    if sessionmanager._engine is not None:
        await sessionmanager.close()


app: FastAPI = application.create(
    debug=settings.debug,
    rest_routers=(rest.users.router, rest.organizations.router),
    lifespan=lifespan,
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_config=None)
