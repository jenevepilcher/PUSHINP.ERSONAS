## error at republican run due to attempt to run two things on multiple threads
## learned that assistant does not answer instantanously. must wait.

from openai import OpenAI
import os
import config
import openai

client = OpenAI(api_key=config.Items.key)

# os.environ["OPENAI_API_KEY"] = config.Items.key
# Set up OpenAI API key
#api_key = config.Items.key
#openai.api_key = api_key

democrat = client.beta.assistants.create(
    name="Democrat",
    instructions="You are a democrat. Answer questions as if you are a democrat",
    tools=[{"type": "code_interpreter"}],
    model="gpt-3.5-turbo-1106"
)

republican = client.beta.assistants.create(
    name="Republican",
    instructions="You are a republican. Answer questions as if you are a republican",
    tools=[{"type": "code_interpreter"}],
    model="gpt-3.5-turbo-1106"
)
#creating thread
thread = client.beta.threads.create()

message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="What do you think about gun rights?"
)


democrat_run = client.beta.threads.runs.create(
  thread_id=thread.id,
  assistant_id=democrat.id,
)

republican_run = client.beta.threads.runs.create(
  thread_id=thread.id,
  assistant_id=republican.id,
)

messages = client.beta.threads.messages.list(
  thread_id=thread.id
)

for message in messages.data:
    if message.role == "assistant" and message.assistant_id == democrat.id:
        print("Democrat Assistant:", message.content)
    elif message.role == "assistant" and message.assistant_id == republican.id:
        print("Republican Assistant:", message.content)
