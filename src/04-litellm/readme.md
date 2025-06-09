## **What Is LiteLLM?**

LiteLLM is a lightweight Python client that unifies access to multiple large-language-model providers under one simple API. Instead of installing and configuring the OpenAI, Anthropic, Hugging Face, and other SDKs separately, you install `litellm`, set a couple of environment variables, and call:

```python
from litellm import completion

# LiteLLM picks up your provider, API key, and base URL automatically
resp = completion(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Hello, world!"}],
    stream=True
)
for chunk in resp:
    print(chunk.choices[0].delta.get("content", ""), end="")
```

All provider-specific setup—authentication, base URLs, streaming protocols, retries—happens under the hood.

## **Why Use LiteLLM?**

1. **Vendor-Agnostic**: Write one client call and switch between OpenAI, Anthropic, Amazon Bedrock, or on-prem models by changing an environment variable.
2. **Automatic Retries & Backoff**: Built‑in error handling against rate limits or network issues.
3. **Unified Streaming**: Use `stream=True` for any supported model—no separate client APIs needed.
4. **Light Dependency**: Keeps your environment lean by avoiding multiple heavy SDKs.

## **Benefits with the OpenAI Agent SDK:**

- **Provider Flexibility**: Agents can fall back between providers without code changes—just update `LITELLM_PROVIDER` and `LITELLM_API_KEY`.
- **Single Configuration**: One `.env` controls both the Agent SDK and LiteLLM (no juggling multiple keys or URLs).
- **Increased Resilience**: LiteLLM’s retry logic integrates seamlessly into tool calls and streaming runs.
- **Rapid Prototyping**: Test new or private models (e.g., fine-tuned LLaMA) without rewriting agent setup.

## **How to Get Started:**

1. **Install** your project dependencies:

   ```bash
   pip install openai-agents[litellm]
   ```

2. **Set up your environment**:

   - Copy `.env.example` to `.env`
   - Add your LLM API key (e.g., `GEMINI_API_KEY`)

3. **Write your code** (example below):

   ```python
   import os
   import asyncio
   from agents import Agent, Runner, function_tool, set_tracing_disabled
   from agents.extensions.models.litellm_model import LitellmModel

   set_tracing_disabled(disabled=True)

   MODEL = 'gemini/gemini-2.0-flash'
   GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

   @function_tool
   def get_weather(city: str) -> str:
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
   ```

4. **Run** your project:

   ```bash
   python litellm_agent.py
   ```

With these steps, you’re ready to leverage LiteLLM’s unified client within the OpenAI Agent SDK for flexible, resilient, and vendor-agnostic AI agents.
