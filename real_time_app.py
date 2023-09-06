import streamlit as st
import datetime,pytz
import pandas as pd
from PIL import Image
from timeplus import *
import json

env = Environment().address(st.secrets["TIMEPLUS_HOST"]).apikey(st.secrets["TIMEPLUS_API_KEY"]).workspace(st.secrets["TIMEPLUS_TENANT"])    

MAX_ROW=10
st.session_state.rows=0
sql='SELECT * FROM sample_data'
st.code(sql, language="sql")
with st.empty():
    query = Query(env=env).sql(query=sql).create()
    col = [h["name"] for h in query.metadata()["result"]["header"]]
    def update_row(row,name):
        data = {}
        for i, f in enumerate(col):
            data[f] = row[i]
        
        df = pd.DataFrame([data], columns=col)
        st.session_state.rows=st.session_state.rows+1
        if name not in st.session_state or st.session_state.rows>=MAX_ROW:
            st.session_state[name] = st.table(df)
            st.session_state.rows=0
        else:
            st.session_state[name].add_rows(df)
            
    # iterate query result
    limit = MAX_ROW*10-1
    count = 0
    for event in query.result():
        if event.event != "metrics" and event.event != "query":
            for row in json.loads(event.data):
                update_row(row,"tail")
                count += 1
                if count >= limit:
                    break
            # break the outer loop too    
            if count >= limit:
                break                
    query.cancel()
    query.delete()

st.write(f"Only the recent {MAX_ROW*10} rows are shown. You can refresh the page to view the latest events.")
