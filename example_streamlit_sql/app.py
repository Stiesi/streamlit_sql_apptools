import streamlit as st
from streamlit_sql import show_sql_ui
from dotenv import load_dotenv
import os
import sys
from datetime import date
from sqlalchemy import select
import pandas as pd

sys.path.append(os.path.abspath("."))
from example_streamlit_sql import restart_db
from example_streamlit_sql import db_jj as db


st.set_page_config("Example streamlit_sql app", layout="wide")
load_dotenv(".env")

restarted_date = restart_db.restart_db()
today = date.today()
if today > restarted_date:
    restart_db.restart_db.clear()  # pyright: ignore
    restart_db.restart_db()

db_path = "sqlite:///./data.db"
conn = st.connection("sql", url=db_path)

header_col1, header_col2 = st.columns([8, 4])
header_col1.header("Example application using streamlit_sql")


btn_col1, btn_col2 = st.sidebar.columns(2)
btn_col1.link_button(
    "Github", url="https://github.com/edkedk99/streamlit_sql", icon=":material/code:"
)
btn_col2.link_button(
    "Docs", url="https://edkedk99.github.io/streamlit_sql/", icon=":material/menu_book:"
)


def User():
    def fill_alternating(row: pd.Series):
        nlen = len(row)
        if (row.name)%2==1:
            res = [ "background-color: lightgrey"] 
        else:
            res = ["background-color: wheat"] 
        return res *nlen
    
    def fill_by_value(row: pd.Series):
        if row.id > 4:
            style = "background-color: cyan"
        else:
            style = "background-color: pink"

        result = [style] * len(row)
        return result
    
    stmt = (
        select(
            db.User.id,
            db.User.user_name,
            db.User.first_name,
            db.User.last_name,
            #db.User.apptools,
        )
        .select_from(db.User)
        #.join(db.AppTool.id)
        #.where(db.AppUser.user_id == db.User.id)
        .order_by(db.User.user_name)
    )
    show_sql_ui(
        conn=conn,
        read_instance=stmt,
        #read_instance=db.User,
        edit_create_model=db.User,
        #rolling_total_column="annual_income",
        available_filter=["user_name", "apptools"],
        base_key="usr",        
        style_fn=fill_alternating,
        update_show_many=True
    )


def Apptool():
    stmt = select(db.AppTool)
    show_sql_ui(
        conn=conn,
        read_instance=stmt,
        edit_create_model=db.AppTool,
        update_show_many=True,
    )

def AppUser_bak():
    stmt = select(db.AppUser)
    show_sql_ui(
        conn=conn,
        read_instance=stmt,
        hide_id=False,
        edit_create_model=db.AppUser,
        update_show_many=True,
    )
def AppUser():
    stmt = select(db.User.id,db.User.user_name,db.User.last_name)
    #.where()
    with conn.session as s:
        data = s.execute(stmt).fetchall()
    #st.dataframe(data)
    df = pd.DataFrame(data,columns=['id','user_','last_name'])
    event = st.dataframe(df,selection_mode='single-row',key="jjdata",on_select='rerun')
    if event.selection['rows']:
        row = event.selection['rows'][0]
        user = df.iloc[row]
        st.write(user)
        with conn.session as s:
            
            apps=s.execute(select(db.AppTool.name).where(db.AppUser.user_id == int(user.id))).fetchall()
            apps = [apt for apt in apps]
            st.write(apps)
    

pages = [
    st.Page(User, title="User Table"),
    st.Page(Apptool, title="Apptool Table"),
    #st.Page(AppUser, title="Apptool- user Table"),
]

page = st.navigation(pages)
page.run()
