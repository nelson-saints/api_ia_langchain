from dotenv import find_dotenv, load_dotenv
import os, openai
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

load_dotenv(find_dotenv())


chat = ChatOpenAI(
    base_url = "https://integrate.api.nvidia.com/v1",
    api_key = os.getenv("NVIDIA_API_KEY"),
    model='nvidia/nemotron-3-nano-omni-30b-a3b-reasoning',
    max_tokens=500,
    temperature=1,
    n=1,
    seed=42
    )

messages = [
    SystemMessage(content="Voce é um programador sênior, que responderá sempre em topicos. Reponda sempre em português do Brasil. Não use inglês, exceto quando termos técnicos ou nomes próprios forem necessários."),
    HumanMessage(content="Me explique o que é python.")
]

response = chat.invoke(messages)
print(response.content)