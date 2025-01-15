import sys
from sqlalchemy.orm import Session
from sqlalchemy import func, select
from sqlalchemy_utils import database_exists
import db_jj as db


def get_userapps(session:Session,user_name: str) -> list[str]:
    user = s.query(db.User).where(db.User.user_name==user_name).first()
    apps = [app.name for app in user.apptools]
    return apps

def add_userapp(session:Session,user_name:str,app_name:str) -> str|None:
    try:
        user = s.query(db.User).where(db.User.user_name==user_name).first()
        app  = s.query(db.AppTool).where(db.AppTool.name==app_name).first()
        add_rel = db.AppUser(user_id=user.id,app_id=app.id)
        session.add(add_rel)
        session.commit()
        #session.flush()
        return add_rel.id
    except:
        return None


def delete_userapp(session:Session,user_name,app_name):
    try:
        user = s.query(db.User).where(db.User.user_name==user_name).first()
        app  = s.query(db.AppTool).where(db.AppTool.name==app_name).first()
        appuser  = s.query(db.AppUser).where(db.AppUser.user_id==user.id).where(db.AppUser.app_id==app.id).first()
        objs = session.execute(select(db.AppUser).where(db.AppUser.user_id==user.id).where(db.AppUser.app_id==app.id)).all()
        session.delete(objs)
        session.commit()
    except:
        print(f'{user_name} - {app_name} not deleted')

if __name__ == "__main__":
    
    #db_path = os.environ["ST_DB_PATH"]
    db_path = "sqlite:///./data.db"
    if not database_exists(db_path):
        print('Database does not exist!')
        sys.exit()
    

    engine = db.new_engine(db_path)


    # test some statements
    # 
    #stmt = select(db.User).filter().limit(5).all()#.join(db.AppUser.user_id, db.User.id).join(db.AppUser.app_id,db.AppTool.id)
    #print(stmt)
    with Session(engine) as s:
        #data = s.execute(stmt)
        #print(data[-1][0])
        stmt= select(db.User).filter_by(id=5)        
        user = s.execute(stmt).first()
        if user is not None:
            user1 = user[0]
            print(f'for user {user1.user_name}')
            print(get_userapps(s,user_name=user1.user_name))
        # apps registered for first user
#        apps = [app.name for app in user1.apptools]
#        print(apps)

        #app1 = s.query(db.AppTool).limit(5).all()[-1]
        app  = s.execute(select(db.AppTool)).all()
        
        # users registered for first app
        app1=app[5][0]
        print(f'for app {app1.name}')
        users = [user.user_name for user in app1.users]
        print(users)

        # add one user to one application
        #user = s.query(db.User).where(db.User.user_name==user1.user_name).first()
        #add_rel = db.AppUser(user_id=user.id,app_id=1)
        if user1 is not None:
            print(add_userapp(s,user1.user_name,app1.name))
        #s.add(add_rel)
        #s.commit()
        #user1 = s.query(db.User).first()
        #user2 = s.query(db.User).where(db.User.user_name==user1.user_name).first()
        
        user = s.execute(stmt).first()
        if user is not None:
            user1 = user[0]

            print(f'for user {user1.user_name}')
            # apps registered for first user
            apps = [app.name for app in user1.apptools]
            print(apps)
        delete_userapp(s,user1.user_name,app1.name)

        apps = [app.name for app in user1.apptools]
        print(apps)