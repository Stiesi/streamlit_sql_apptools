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
    def fill_by_2(row: pd.Series):
        nlen = len(row)
        res = [ "background-color: cyan" if i%2==1 else "background-color: pink" for i in range(nlen)] 
        return res
    
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
        style_fn=fill_by_2,
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

def AppUser():
    stmt = (select(db.User.user_name,
                  db.AppTool.name).select_from(db.User)
                .join(db.AppUser)
    )
    show_sql_ui(
        conn=conn,
        read_instance=stmt,
        edit_create_model=db.AppUser,
        update_show_many=True,
    )


pages = [
    st.Page(User, title="User Table"),
    st.Page(Apptool, title="Apptool Table"),
    #st.Page(AppUser, title="Apptool- user Table"),
]

page = st.navigation(pages)
page.run()
