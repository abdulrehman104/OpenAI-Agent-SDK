# ————————————————————————————————  LiteLLM With Multiple LLMs ————————————————————————————————
import os
import asyncio
from litellm import completion
from agents import Agent, Runner, function_tool, set_tracing_disabled
from agents.extensions.models.litellm_model import LitellmModel


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")


def gemini():
    response = completion(
        model="gemini/gemini-1.5-flash",
        messages=[{ "content": "Hello, how are you?","role": "user"}],
        api_key=GEMINI_API_KEY
    )

    print(response)

def gemini2():
    response = completion(
        model="gemini/gemini-2.0-flash-exp",
        messages=[{ "content": "Hello, what is biryani","role": "user"}],
        api_key=GEMINI_API_KEY
    )

    print(response.choices[0].message.content)


def openai():
    response = completion(
        model="openai/gpt-4o",
        messages=[{ "content": "Hello, how are you?","role": "user"}],
        api_key=OPENAI_API_KEY

    )

    print(response)

def antropic():
    response = completion(
      model="anthropic/claude-3-sonnet-20240229",
      messages=[{ "content": "Hello, how are you?","role": "user"}],
      api_key=ANTHROPIC_API_KEY
    )

    print(response)


gemini()
gemini2()
openai()
antropic()


# ————————————————————————————————  LiteLLM With OpenAI Agent SDK (Function Run sync) ————————————————————————————————

set_tracing_disabled(disabled=True)

MODEL = 'gemini/gemini-1.5-flash'
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


@function_tool
def get_weather(city: str)->str:
    print(f"[debug] getting weather for {city}")
    return f"The weather in {city} is sunny."


def main(model: str, api_key: str):
  agent = Agent(
      name="Assistant",
      instructions="You only respond in haikus.",
      model=LitellmModel(model=model, api_key=api_key),

  )

  result = Runner.run_sync(agent, "What's the weather in Tokyo?")
  print(result.final_output)


main(model=MODEL, api_key=GEMINI_API_KEY)


# ————————————————————————————————  LiteLLM With OpenAI Agent SDK (Function Run async) ————————————————————————————————

set_tracing_disabled(disabled=True)

MODEL = 'gemini/gemini-2.0-flash'
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")



@function_tool
def get_weather(city: str)->str:
    print(f"[debug] getting weather for {city}")
    return f"The weather in {city} is sunny."


async def main(model: str, api_key: str):
  agent = Agent(
      name="Assistant",
      instructions="You only respond in haikus.",
      model=LitellmModel(model=model, api_key=api_key),

  )

  result = await Runner.run(agent, "What's the weather in Tokyo?")
  print(result.final_output)


asyncio.run(main(model=MODEL, api_key=GEMINI_API_KEY))
