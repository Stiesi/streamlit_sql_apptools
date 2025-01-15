
from sqlmodel import Field, SQLModel, Relationship, create_engine 


#class Hero(SQLModel, table=True):  
#    id: int | None = Field(default=None, primary_key=True)  
#    name: str  
#    secret_name: str  
#    age: int | None = None  


class User(SQLModel, table=True):
    id: int | None = Field(default=None,primary_key=True)
    user_name: str = Field(index=True)
    first_name: str 
    last_name: str
    is_active: bool = Field(default=False)
    is_admin: bool = Field(default=False)

    #apptools: list["AppTool"] = Relationship(link_model="AppUserLink",back_populates="users")

    #def __str__(self):
    #    return self.user_name

class AppTool(SQLModel,table=True):
    id: int | None = Field(default=None,primary_key=True)
    name: str = Field(index=True)
    link_prod: str
    link_git: str  = Field(index=True)

    
    keyuser: int | None = Field(default=None, foreign_key="user.id")

    #users: list[User] = Relationship(link_model="AppUserLink",back_populates="apptools")

    #def __str__(self) -> str:
    #    return f"{self.name}, {self.keyuser}"

'''
class AppUserLink(SQLModel,table=True):
    #__tablename__="_appuser"
    #id: Mapped[int] = mapped_column(primary_key=True)
    #name: Mapped[str] # just for streamlit_sql
    user_id: int| None = Field(default=None,foreign_key="user.id",primary_key=True)
    app_id:  int| None = Field(default=None,foreign_key="apptool.id",primary_key=True)

    #def __str__(self):
    #    return f"{self.user_id} , {self.app_id}"
    
    #def __repr__(self):
    #    return f"{self.user_id} , {self.app_id}"

'''


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

if __name__=='__main__':
    SQLModel.metadata.create_all(engine)
