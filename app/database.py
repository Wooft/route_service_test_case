from flask_sqlalchemy import SQLAlchemy, session
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from manage import app

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://127.0.0.1:5000"
class Base(DeclarativeBase):
  pass

db = SQLAlchemy(app, model_class=Base)

class User(db.Model):
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(db.String, unique=True, nullable=False)

with app.app_context():
    db.create_all()
    db.session.add(User(username='example'))
    db.session.commit()
    users = db.session.execute(db.select(User)).scalars()