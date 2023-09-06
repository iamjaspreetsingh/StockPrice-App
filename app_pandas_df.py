from langchain.agents import create_pandas_dataframe_agent
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_types import AgentType
import streamlit as st
from langchain.llms import OpenAI
import pandas as pd
import os

os.environ["OPENAI_API_KEY"]=st.secrets["OPENAI_API_KEY"]

df = pd.read_csv("survey.csv")

agent = create_pandas_dataframe_agent(OpenAI(temperature=0), df, verbose=True)

agent = create_pandas_dataframe_agent(
    ChatOpenAI(temperature=0.7, model="gpt-3.5-turbo-0613"),
    df,
    verbose=True,
    agent_type=AgentType.OPENAI_FUNCTIONS,
)

agent.run("how many rows are there?")



