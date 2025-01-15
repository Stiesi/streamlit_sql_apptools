import streamlit as st
from streamlit_sql import show_sql_ui
from dotenv import load_dotenv
import os
import sys
from datetime import date
from sqlalchemy import select,delete
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
        if (row.name)%2==1: # pyright: ignore
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
            db.User.is_active,
            db.User.is_admin,
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
        edit_create_default_values={"is_active":True},
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
def button_type():
    #st.write(st.session_state["Update-app_user"])#.type='secondary'
    pass

def AppUser():
    
    from streamlit_sql import create_delete_model, lib, read_cte, update_model
    from sqlalchemy import CTE, Select, select

    read_instance=db.AppUser
    if isinstance(read_instance, Select):
        cte = read_instance.cte()
    elif isinstance(read_instance, CTE):
        cte = read_instance
    else:
        cte = select(read_instance).cte()
    ss = st.session_state
    available_filter=[]

    lib.set_state("stsql_updated", 1)
    lib.set_state("stsql_update_ok", None)
    lib.set_state("stsql_update_message", None)
    lib.set_state("stsql_opened", False)

    header_container = st.container()
    data_container = st.container()
    pag_container = st.container()

    table_name = lib.get_pretty_name(db.AppUser.__tablename__)
    header_container.header(table_name, divider="orange")

    expander_container = header_container.expander(
        "Filter",
        icon=":material/search:",
    )
    filter_container = header_container.container()
    saldo_toggle_col, saldo_value_col = header_container.columns(2)
    btns_container = header_container.container()

    if ss.stsql_update_ok is True:
        header_container.success(ss.stsql_update_message, icon=":material/thumb_up:")
    if ss.stsql_update_ok is False:
        header_container.error(ss.stsql_update_message, icon=":material/thumb_down:")

    filter_colsname = available_filter
    if len(filter_colsname) == 0:
        filter_colsname = [col.description for col in cte.columns if col.description]


#######################
    stmt = select(db.User.id,db.User.user_name,db.User.last_name)
    #stmt = select(db.AppTool).select().id,db.User.user_name,db.User.last_name)
    #.where()
    with conn.session as s:
        data = s.execute(stmt).fetchall()
    #st.dataframe(data)
    df = pd.DataFrame(data,columns=['id','user_','last_name'])
    event = st.dataframe(df,selection_mode='single-row',key="jjdata",on_select='rerun')
    if event.selection['rows']: # pyright: ignore
        row = event.selection['rows'][0]  # pyright: ignore
        user = df.iloc[row]
        user_id = int(user.id)
        st.write(user)
        with conn.session as s:
            
            #apps=s.execute(select(db.AppTool.name).where(db.AppUser.user_id == int(user.id))).fetchall()
            stmt = (
                select(db.AppTool)
                .join(db.AppUser, db.AppUser.app_id == db.AppTool.id)
                .join(db.User, db.User.id == db.AppUser.user_id)
                .where(db.User.id == user_id)
            )
            apps_assigned=s.execute(stmt).scalars().all()
            apps = [apt.name for apt in apps_assigned]
            allapps = s.execute(select(db.AppTool.name)).scalars().all()
            newapps = st.multiselect('Apps assigned',options=allapps,default=apps,on_change=button_type)
            #st.write(newapps)
        
            update = st.button('Update',type='primary',key='Update-app_user')
            if update:
                #for app_user in apps_assigned:
                delstmt = (delete(db.AppUser)
                            .where(db.AppUser.user_id==user_id))
                s.execute(delstmt)
                #s.delete(apps_assigned)
                s.commit()
                
                for app_name in newapps:
                    apptool = s.execute(select(db.AppTool).where(db.AppTool.name==app_name)).fetchone()
                    apptool_id = apptool[0].id  # pyright: ignore
                    new_app_user = db.AppUser(user_id=user_id,app_id=apptool_id)                
                    #st.write(apptool)
                    s.add(new_app_user)                    
                s.commit()
                st.toast('updated')
                #st.session_state["Update-app_user"].type='secondary'


    

pages = [
    st.Page(User, title="User Table"),
    st.Page(Apptool, title="Apptool Table"),
    st.Page(AppUser, title="work"),
    st.Page(AppUser_bak, title="Apptool- user Table"),
]

page = st.navigation(pages)
page.run()
