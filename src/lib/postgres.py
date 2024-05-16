
from sqlalchemy.ext.asyncio import async_sessionmaker, async_scoped_session
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base
from asyncio import current_task

Base = declarative_base()

class Model(Base):
    __abstract__ = True
    __table_args__ = {'extend_existing': True}

    @property
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Postgres:
    def __init__(self, url: str, *args, **kwargs) -> None:
        super(Postgres, self).__init__(*args, ** kwargs)
        self.engine = create_async_engine(url=url, pool_pre_ping=True, pool_size=2000, max_overflow=100)
        self.session = self._make_session()
        self.Model = Model

    def _make_session(self):
        factory = async_sessionmaker(bind=self.engine)
        return async_scoped_session(factory, current_task)

    async def create_all(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(self.Model.metadata.create_all)