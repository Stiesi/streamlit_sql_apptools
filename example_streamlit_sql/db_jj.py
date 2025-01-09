import os
from dotenv import load_dotenv

from sqlalchemy import Engine, ForeignKey
#, create_engine,PrimaryKeyConstraint
from sqlalchemy.engine.url import make_url
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)
from sqlalchemy_utils import create_database, database_exists
from sqlalchemy.orm import sessionmaker

from sqlmodel import Field, SQLModel, create_engine  


class Base(DeclarativeBase):
    pass

class SBase(SQLModel):
    pass

class User(Base):
    __tablename__ = "user_table"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_name: Mapped[str] = mapped_column(unique=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=False)
    is_admin: Mapped[bool] = mapped_column(default=False)

    #apptools_ids: Mapped[int] = mapped_column(ForeignKey("apptool_table.id"))

    #apptools: Mapped[list["AppTool"]] = relationship(back_populates="users")
    apptools: Mapped[list["AppTool"]] = relationship(secondary="_appuser",back_populates="users")

    def __str__(self):
        return self.user_name

class AppTool(Base):
    __tablename__ = "apptool_table"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(index=True)
    link_prod: Mapped[str]
    link_git: Mapped[str]  = mapped_column(unique=True)

    #users: Mapped[list["User"]] = relationship(secondary="_appuser",back_populates="apptools")
    #user_ids: Mapped[int] = mapped_column(ForeignKey("user.id"))
    
    keyuser: Mapped[User] = mapped_column(ForeignKey("user_table.id"))

    users: Mapped[list[User]] = relationship(secondary="_appuser",back_populates="apptools")

    def __str__(self) -> str:
        return f"{self.name}, {self.keyuser}"


class AppUser(Base):
    __tablename__="_appuser"
    id: Mapped[int] = mapped_column(primary_key=True)
    #name: Mapped[str] # just for streamlit_sql
    user_id: Mapped[int] = mapped_column(ForeignKey("user_table.id"))
    app_id:  Mapped[int] = mapped_column(ForeignKey("apptool_table.id"))

    def __str__(self):
        return f"{self.user_id} , {self.app_id}"
    
    def __repr__(self):
        return f"{self.user_id} , {self.app_id}"


def new_engine(db_path: str):
    engine = create_engine(db_path)
    return engine


def create_tables(engine: Engine):
    Base.metadata.create_all(engine)


db_path = "sqlite:///./data.db"
if not database_exists(db_path):
    create_database(db_path)
    url = make_url(db_path)
    print(
        f"Database created on {url.host}, port {url.port}, database {url.database}"
    )

db = new_engine(db_path)

SessionLocal = sessionmaker(bind=db)
print (f'Session created')
try:
    print (f'name {db.name}')
    print (f'host {db.url.host}')
    #print(SessionLocal.info()) 
except:
    print('Error in sessionmaker')

def get_db():
    db = SessionLocal()
    try:
        yield db        
    finally:
        db.close()

if __name__ == "__main__":
    #db_path = "sqlite:///./data.db"
    #if not database_exists(db_path):
    #    create_database(db_path)
    #    url = make_url(db_path)
    #    print(
    #        f"Database created on {url.host}, port {url.port}, database {url.database}"
    #    )

    #engine = new_engine(db_path)
    create_tables(db)
    print("created")
