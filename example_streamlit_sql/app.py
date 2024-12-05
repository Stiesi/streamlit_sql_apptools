import streamlit as st
from streamlit_sql import ModelOpts, show_sql_ui
from dotenv import load_dotenv
import os
from example_streamlit_sql import db, restart_db

st.set_page_config("Example streamlit_sql app", layout="wide")
load_dotenv(".env")
deploy = os.environ["DEPLOY"]

if deploy == "cloud":
    restart_db.restart_db()

db_path = "sqlite:///data.db"
conn = st.connection("sql", url=db_path)

st.header("Example application using streamlit_sql")

address_model = ModelOpts(db.Address)
person_model = ModelOpts(
    Model=db.Person,
    rolling_total_column="annual_income",
    read_use_container_width=True,
)

models = [address_model, person_model]
show_sql_ui(conn, models)
