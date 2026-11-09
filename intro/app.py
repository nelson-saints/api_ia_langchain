import openai
import os
from dotenv import load_dotenv, find_dotenv
from pprint import pprint
load_dotenv(find_dotenv())

client = openai.Client(
    base_url = "https://integrate.api.nvidia.com/v1",
      api_key = os.getenv("NVIDIA_API_KEY")
    )

prompt = [
    {'role': 'user', 'content': 'Descreva a linguagem python com todos os detalhes possiveis.'}
]

        
        
def stream_chat_response():
    
    response = client.chat.completions.create(
    messages=prompt,
    #model='nvidia/nemotron-3.5-super-vl-120b-a12b',
    model='nvidia/nemotron-3-nano-omni-30b-a3b-reasoning',
        max_tokens=500,
        temperature=0.5,
        n=1,
        seed=42,
        stream=True
    )

    # print(response.choices[0].message.content)
    # print(response.usage)
    #pprint(response.choices[0].message.model_dump(exclude_none=True), depth=3)

    for chunk in response:
        content = chunk.choices[0].delta.content
        if content:
            yield content
            
    print(chunk.usage)


for i in stream_chat_response():
    print(i, end='')
