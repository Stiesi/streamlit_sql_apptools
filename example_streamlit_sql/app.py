import streamlit as st
from streamlit_sql import ModelOpts, show_sql_ui
from dotenv import load_dotenv
import os
import sys
from datetime import date

sys.path.append(os.path.abspath("."))
from example_streamlit_sql import db, restart_db


st.set_page_config("Example streamlit_sql app", layout="wide")
load_dotenv(".env")

restarted_date = restart_db.restart_db()
today = date.today()
if today > restarted_date:
    restart_db.clear()  # pyright: ignore
    restart_db.restart_db()

db_path = "sqlite:///data.db"
conn = st.connection("sql", url=db_path)

header_col1, header_col2 = st.columns([8, 4])
header_col1.header("Example application using streamlit_sql")
with header_col2.popover("Show the code"):
    st.code(
        """
    address_model = ModelOpts(db.Address)
    person_model = ModelOpts(
        Model=db.Person,
        rolling_total_column="annual_income",
        read_use_container_width=True,
    )

    models = [address_model, person_model]
    show_sql_ui(conn, models)
    """,
        language="python",
        line_numbers=True,
    )


btn_col1, btn_col2 = st.sidebar.columns(2)
btn_col1.link_button(
    "Github", url="https://github.com/edkedk99/streamlit_sql", icon=":material/code:"
)
btn_col2.link_button(
    "Docs", url="https://edkedk99.github.io/streamlit_sql/", icon=":material/menu_book:"
)

address_model = ModelOpts(db.Address)
person_model = ModelOpts(
    Model=db.Person,
    rolling_total_column="annual_income",
    read_use_container_width=True,
)

models = [address_model, person_model]
show_sql_ui(conn, models)
