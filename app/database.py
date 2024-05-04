import atexit
from decouple import config
from sqlalchemy import Column, String, Integer, DateTime, create_engine, JSON, ForeignKey, Float
from sqlalchemy.orm import sessionmaker, DeclarativeBase

PG_DSN = f"postgresql://{config('DB_USER')}:{config('DB_PASSWORD')}@127.0.0.1/{config('DB_NAME')}"
engine = create_engine(PG_DSN)
Session = sessionmaker(engine)
atexit.register(engine.dispose)

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=False, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, autoincrement=True)

    def __str__(self):
        return self.username


class Routes(Base):
    __tablename__ = 'routes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    start_time = Column(DateTime)
    duration = Column(Float)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String, nullable=True)
    route_points = Column(JSON)
    distance = Column(Float)
    end_time = Column(DateTime)

    @property
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'duration': self.duration,
            'distance': self.distance,
            'route': self.route_points,
            'start_time': self.start_time,
            'end_time': self.end_time
        }

if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)