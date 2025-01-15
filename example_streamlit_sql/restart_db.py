from faker import Faker
#from example_streamlit_sql import db_jj as db
import db_jj as db
from dotenv import load_dotenv
import os
from sqlalchemy.orm import Session
from sqlalchemy import func, select
from sqlalchemy_utils import database_exists
import streamlit as st
from datetime import date


def create_user(session: Session):
    Faker.seed(100)
    fake = Faker()    
    for i in range(100):
        user = db.User(
            user_name=fake.unique.user_name(),
            last_name=fake.last_name(),
            first_name=fake.first_name(),
            #apptools_ids=[]
        )
        session.add(user)

    session.commit()


def create_apptool(session: Session):
    Faker.seed(100)
    fake = Faker()    
    for i in range(10):
#        stmt = select(db.AppTool.id).order_by(func.random()).limit(1)
#        user_id = session.execute(stmt).scalar_one()

        apptool = db.AppTool(
            name=fake.unique.word(),
            link_prod=fake.uri_path(),
            link_git=fake.unique.url(),  
            keyuser=fake.user_name()          
        )
        session.add(apptool)

    session.commit()

def create_appuser(session: Session):
    Faker.seed(100)
    fake = Faker()
    for i in range(100):
        stmt = select(db.AppTool.id).order_by(func.random()).limit(1)
        apptool_id = session.execute(stmt).scalar_one()
        stmt = select(db.User.id).order_by(func.random()).limit(1)
        user_id = session.execute(stmt).scalar_one()

        appuser = db.AppUser(
            user_id = user_id,
            app_id=apptool_id,
        )
        session.add(appuser)

    session.commit()



@st.cache_resource
def restart_db():
    print("Creating sqlite database and generating fake data")
    db_path = "sqlite:///./data.db"
    if not database_exists(db_path):
        engine = db.new_engine(db_path)
        db.Base.metadata.drop_all(engine)
        db.Base.metadata.create_all(engine)

        with Session(engine) as s:
            create_user(s)
            create_apptool(s)
            create_appuser(s)

    today = date.today()
    return today


if __name__ == "__main__":
    load_dotenv(".env")
    #db_path = os.environ["ST_DB_PATH"]
    db_path = "sqlite:///./data.db"
    engine = db.new_engine(db_path)

    if 1:
        db.Base.metadata.drop_all(engine)
        db.Base.metadata.create_all(engine)
        with Session(engine) as s:
            create_user(s)
            create_apptool(s)
            create_appuser(s)

    # test some statements
    # 
    stmt = select(db.User)#.join(db.AppUser.user_id, db.User.id).join(db.AppUser.app_id,db.AppTool.id)
    print(stmt)
    with Session(engine) as s:
        data = s.execute(stmt).all()
        print(data[0][0])
        user1 = s.query(db.User).first()
        apps = [app.name for app in user1.apptools]
        print(apps)

        app1 = s.query(db.AppTool).first()
        apps = [user.user_name for user in app1.users]
        print(apps)