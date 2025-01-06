import os
from dotenv import load_dotenv

from sqlalchemy import Engine, ForeignKey, create_engine
from sqlalchemy.engine.url import make_url
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)
from sqlalchemy_utils import create_database, database_exists


class Base(DeclarativeBase):
    pass


class AppTool(Base):
    __tablename__ = "apptool"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(index=True)
    link_prod: Mapped[str]
    link_git: Mapped[str]  = mapped_column(unique=True)

    users: Mapped[list["User"]] = relationship(secondary="_appuser",back_populates="apptools")

    def __str__(self) -> str:
        return f"{self.name}, {self.link_git}"


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_name: Mapped[str] #= mapped_column(unique=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=False)
    is_admin: Mapped[bool] = mapped_column(default=False)

    apptools: Mapped[list["AppTool"]] = relationship(secondary="_appuser",back_populates="users")

    def __str__(self):
        return self.user_name

class AppUser(Base):
    __tablename__="_appuser"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    app_id:  Mapped[int] = mapped_column(ForeignKey("apptool.id"))

    def __str__(self):
        return f"{self.user_id} , {self.app_id}"



def new_engine(db_path: str):
    engine = create_engine(db_path)
    return engine


def create_tables(engine: Engine):
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    db_path = "sqlite:///./data.db"
    if not database_exists(db_path):
        create_database(db_path)
        url = make_url(db_path)
        print(
            f"Database created on {url.host}, port {url.port}, database {url.database}"
        )

    engine = new_engine(db_path)
    create_tables(engine)
    print("criado")
