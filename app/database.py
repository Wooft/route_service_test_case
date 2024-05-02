import atexit
from decouple import config
from sqlalchemy import Column, String, Integer, DateTime, create_engine, JSON, ForeignKey
from sqlalchemy.orm import sessionmaker, DeclarativeBase

PG_DSN = f"postgresql://{config('DB_USER')}:{config('DB_PASSWORD')}@localhost/{config('DB_NAME')}"
engine = create_engine(PG_DSN)
Session = sessionmaker(engine)
atexit.register(engine.dispose)

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=False, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, autoincrement=True)

    def __str__(self):
        return self.name

class Routes(Base):
    __tablename__ = 'routes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String, nullable=True)
    json_data = Column(JSON)

    @property
    def to_dict(self):
        return {
            'id': self.id,
            'route': self.json_data
        }

if __name__ == '__main__':
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)