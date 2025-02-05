import contextlib
import json
from typing import Any, AsyncIterator, Annotated

import orjson
from fastapi import Depends
from sqlalchemy import event
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    AsyncConnection,
    async_sessionmaker,
    create_async_engine,
)

from src.config import settings
from src.infrastructure.database import ActivityTable

__all__ = ("engine", "DBSessionDep", "get_db_session", "sessionmanager")

from src.infrastructure.errors import DatabaseError

CONNECTION_TYPES_CODES = (
    ("json", json.dumps, orjson.loads, "pg_catalog"),
    ("jsonb", json.dumps, orjson.loads, "pg_catalog"),
)

engine: AsyncEngine = create_async_engine(
    settings.database.url, future=True, pool_pre_ping=True, echo=False
)


@event.listens_for(engine.sync_engine, "connect")
def register_custom_types(dbapi_connection, *args):
    for typename, encoder, decoder, schema in CONNECTION_TYPES_CODES:
        dbapi_connection.run_async(
            lambda connection: connection.set_type_codec(
                typename=typename,
                encoder=encoder,
                decoder=decoder,
                schema=schema,
            )
        )


@event.listens_for(ActivityTable, "before_insert")
@event.listens_for(ActivityTable, "before_update")
def validate_activity_nesting_level(mapper, connection, target):
    target.validate_nesting_level()


class DatabaseSessionManager:
    def __init__(self, host: str, engine_kwargs: dict[str, Any] = {}):
        self._engine = create_async_engine(host, **engine_kwargs)
        self._sessionmaker = async_sessionmaker(
            autocommit=False, bind=self._engine, expire_on_commit=False
        )

    async def close(self):
        if self._engine is None:
            raise DatabaseError(message="DatabaseSessionManager is not initialized")
        await self._engine.dispose()

        self._engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise DatabaseError(message="DatabaseSessionManager is not initialized")

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise DatabaseError(message="DatabaseSessionManager is not initialized")

        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


sessionmanager = DatabaseSessionManager(settings.database.url)


async def get_db_session():
    async with sessionmanager.session() as session:
        yield session


DBSessionDep = Annotated[AsyncSession, Depends(get_db_session)]
