
import os
import requests
import json
import asyncio
from openai import AsyncOpenAI
from agents import Agent, Runner, set_tracing_disabled, OpenAIChatCompletionsModel


# ———————————————————————————————— OpenRouter With LLMs ————————————————————————————————

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
BASE_URL = "https://openrouter.ai/api/v1"
# MODEL = "google/gemini-2.0-flash-001"
MODEL = "deepseek/deepseek-chat-v3-0324:free"
# MODEL = "mistralai/mistral-small-24b-instruct-2501:free"


# ——————————————————— Using the OpenRouter API directly ———————————————————

response = requests.post(
  url="https://openrouter.ai/api/v1/chat/completions",
  headers={
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
  },
  data=json.dumps({
    "model": MODEL,
    "messages": [
      {
        "role": "user",
        "content": "What is the meaning of life?"
      }
    ]
  })
)

# print(response.json())

data = response.json()
print(data['choices'][0]['message']['content'])


# ———————————————————————————————— Using OpenRouter With OpenAI Agent SDK ————————————————————————————————

client = AsyncOpenAI(base_url=BASE_URL, api_key=OPENROUTER_API_KEY)

async def main():
  agent = Agent(
      name="Assistant",
      instructions="You are a helpfull AI Assistant",
      model=OpenAIChatCompletionsModel(model=MODEL, openai_client=client),
  )

  result = await Runner.run(agent, "What is the meaning of life?")
  print(result.final_output)

asyncio.run(main())




# https://openrouter.ai/                     ----> (Website)
# https://openrouter.ai/docs/quickstart      ----> (Docs)
# https://github.com/panaversity/learn-agentic-ai/tree/main/01_ai_agents_first/02_openrouter ----> (Repo)
# https://colab.research.google.com/drive/1LOEOBP52WJpmMWsOS7-SUDQBLtmXZ_1d?usp=sharing#scrollTo=xrJVAu7cwe5u ----> (Google Collab)

# Some other free models:
# https://openrouter.ai/deepseek/deepseek-chat-v3-0324:free
# https://openrouter.ai/google/gemini-2.5-pro-exp-03-25:free