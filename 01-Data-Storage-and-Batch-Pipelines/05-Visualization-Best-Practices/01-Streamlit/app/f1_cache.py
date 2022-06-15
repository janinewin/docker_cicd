import streamlit as st

__all__ = [
    'F1Cache'
]

class F1Cache:
    def cacheKeyValue(self, key, value):
        st.session_state[key] = value
    
    def getValueForKey(self, key):
        if key not in st.session_state:
            self.cacheKeyValue(key, None)
        return st.session_state[key]
    
if __name__ == '__main__':
    cache = F1Cache()
