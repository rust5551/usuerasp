from sqlalchemy import create_engine
from sqlalchemy import String
from sqlalchemy import select
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Session

class Base(DeclarativeBase):
    pass

engine = create_engine("sqlite+pysqlite:///users.db", echo=True)

class Users(Base): #База данных
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(String())
    name: Mapped[str] = mapped_column(String())
    group: Mapped[str] = mapped_column(String())


def add_user(id: str, name: str, group: str=""):
    with Session(engine) as session:
        user = Users(
            id = id,
            name = name)

        session.add(user)
        session.commit()

def change_group(id: str, group:str):
    with Session(engine) as session:
        stmt = select(Users).where(Users.id == id)
        user = session.scalar(stmt)

        user.group = group
        session.commit()


Base.metadata.create_all(engine)