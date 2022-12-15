import streamlit as st

class F1Cache:
    def cache_key_value(self, key, value):
        st.session_state[key] = value

    def get_value_for_key(self, key):
        if key not in st.session_state:
            self.cache_key_value(key, None)
        return st.session_state[key]
