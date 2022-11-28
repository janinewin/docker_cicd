import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL

__all__ = ["F1Database"]


class F1Database:
    def __init__(
        self,
    ) -> None:
        self.db_connection = self.init_connection(URL.create(**st.secrets["postgres"]))

    @st.experimental_singleton
    def init_connection(_self, credentials):
        conn = create_engine(credentials, echo=False)
        return conn
