from fastapi import FastAPI, Request, Form, Response
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import CTransformers
from langchain.chains import ConversationalRetrievalChain
from langchain import PromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from langchain.tools import DuckDuckGoSearchRun, DuckDuckGoSearchResults
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser,JsonKeyOutputFunctionsParser

local_file_path = 'datafromazure.csv'
DB_FAISS_PATH = 'vectorstore4/db_faiss'

app = FastAPI()
search = DuckDuckGoSearchRun()
# search = DuckDuckGoSearchResults(backend="news")

#Loading the model
def load_llm():
    llm = CTransformers(
        model = "mistral-7b-instruct-v0.1.Q8_0.gguf", # "mistral-7b-v0.1.Q8_0.gguf",#"llama-2-7b-chat.ggmlv3.q8_0.bin", #"codellama-13b-instruct.Q8_0.gguf"
        model_type="mistral", #"llama"
        max_new_tokens = 1048,
        repetition_penalty=1.13,
        temperature = 0
    )
    return llm

loader = CSVLoader(file_path=local_file_path, encoding="utf-8", csv_args={
            'delimiter': ','})
data = loader.load()
# print(data)
embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2',
                                    model_kwargs={'device': 'cpu'})

db = FAISS.from_documents(data, embeddings)
db.save_local(DB_FAISS_PATH)
llm = load_llm()
chain = ConversationalRetrievalChain.from_llm(llm=llm, retriever=db.as_retriever())

session_state_history = []

custom_prompt_template = """

Question based on data: {question}

Stock dataset is provided for last 1 week for each stock name.
Use the stock dataset provided only to answer the user's question.
If you are not able to find the answer in the dataset provided, just say that you don't know, don't try to make up an answer.
Only return the accurate answer based on dataset and nothing else.

"""


def get_result(query):

    print("Chain started")

    prompt = PromptTemplate(template=custom_prompt_template, input_variables=["question"])
    result = chain.invoke({"question": query, "prompt": prompt, "chat_history": session_state_history}) # LCEL invoke() method used

    answer=result['answer']
    print(answer)

    json_response = (
        ChatPromptTemplate.from_template("Extract the stock name(s) talked about in sentence below. Just mention the 'Response' as stock name(s) only. No other text to be returned. Text provided:: \n \"{responsellm1}\"  Response:: ")
        | llm
        # | {"Stock Name": RunnablePassthrough()}
        | RunnablePassthrough()
        | StrOutputParser()
        | search
    )

    answer2 = json_response.invoke({"responsellm1": result["answer"]})
    print("lcel chain")
    print(answer2)

    return answer,answer2



@app.get("/")
async def index(request: Request):
    return "Connection established with Stock data. Ask your question on data"

@app.post("/get_answer")
async def get_answer(request: Request, question: str = Form(...)):
    print(question)
    answer,answer2 = get_result(question)
    final_result = "Question: "+ question +"\n----------------\n Answer by LLM: " + answer+"\n----------------\n News on stock:" +answer2
    res = Response(final_result)
    print("\n\n")
    print(res)
    return res

# uvicorn app:app
# which stock name do you see in data as less profitable?
# Which stock should I buy if I am looking for less risk and gradual profit according to data?
