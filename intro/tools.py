import openai
import os
import json
import requests
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

client = openai.Client(
    base_url = "https://integrate.api.nvidia.com/v1",
      api_key = os.getenv("NVIDIA_API_KEY")
    )

messages = [
    {
        "role": "system",
        "content": (
            "Responda sempre em português do Brasil. "
            "Não use inglês, exceto quando termos técnicos ou nomes próprios forem necessários."
        ),
    },
    {'role': 'user', 'content': 'Me explique as últimas issues abertas em openai/openai-python no github.'}
    ]

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_github_issues",
            "description": "Busca as issues abertas em um repositório do GitHub.",
            "parameters": {
                "type": "object",
                "properties": {
                    "owner": {
                        "type": "string",
                        "description": "Usuário ou organização. Ex: 'openai'"
                    },
                    "repo": {
                        "type": "string",
                        "description": "Nome do repositório. Ex: 'openai-python'"
                    }
                },
                "required": ["owner", "repo"]
            }
        }
    }
]



response = client.chat.completions.create(
     messages=messages,
        #model='nvidia/nemotron-3.5-super-vl-120b-a12b',
        model='nvidia/nemotron-3-nano-omni-30b-a3b-reasoning',
            max_tokens=500,
            temperature=1,
            n=1,
            seed=42,
            tools=tools,
            tool_choice='auto'
)

tool_call = response.choices[0].message.tool_calls[0]
args = json.loads(tool_call.function.arguments)

def get_github_issues(owner, repo):
    url = f'https://api.github.com/repos/{owner}/{repo}/issues'
    response = requests.get(url)
    issues = response.json()
    return "\n".join([f"- {issue['title']}" for issue in issues [:5]])  # Retorna apenas os 5 primeiros títulos de issues

functions = {
    'get_github_issues': get_github_issues
}

function_execute = functions.get(tool_call.function.name)
result = function_execute(**args)

response = client.chat.completions.create(
     messages=[*messages,
               response.choices[0].message,
               {'role': 'tool',
                'tool_call_id': tool_call.id,
                'content': result}],
        #model='nvidia/nemotron-3.5-super-vl-120b-a12b',
        model='nvidia/nemotron-3-nano-omni-30b-a3b-reasoning',
            temperature=1,
            n=1,
            seed=42,
)

print(response.choices[0].message.content)