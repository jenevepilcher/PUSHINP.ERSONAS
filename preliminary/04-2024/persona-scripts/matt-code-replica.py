## no data out of any messages - lines 37 and 57

import os
import time
import config
from openai import OpenAI

client = OpenAI(api_key=config.Items.key)

api_key = config.Items.key

assistant = client.beta.assistants.create(
    name="Impersonator",
    instructions="Your job is to impersonate an individual based on the information provided.",
    model="gpt-3.5-turbo-1106"
)

thread1 = client.beta.threads.create() # Republican
thread2 = client.beta.threads.create() # Democrat


run = client.beta.threads.runs.create(
  thread_id=thread1.id, # Use `thread1` for our republican thread
  assistant_id=assistant.id,
  instructions="You are an extreme republican with very prolife opinions."
)

run = client.beta.threads.runs.retrieve(
  thread_id=thread1.id,
  run_id=run.id
)

messages = client.beta.threads.messages.list(
  thread_id=thread1.id
)
time.sleep(5)
print(messages)


run = client.beta.threads.runs.create(
  thread_id=thread1.id, # Use `thread1` for our republican thread
  assistant_id=assistant.id,
  instructions="You are presented with an article from the New York Times which strong supports women's right to choose. Would you share this from your personal Twitter account?"
)

run = client.beta.threads.runs.retrieve(
  thread_id=thread1.id,
  run_id=run.id
)
print(run)

messages = client.beta.threads.messages.list(
  thread_id=thread1.id
)

time.sleep(45)
print(messages)

#democrat repeat
run = client.beta.threads.runs.create(
  thread_id=thread2.id, # The only thing that has changed is this line, which now uses `thread2`
  assistant_id=assistant.id,
  instructions="You are an extreme democrat with very strong views in favor of abortion in support of women's right to choose."
)
run = client.beta.threads.runs.retrieve(
  thread_id=thread2.id, # The only thing that has changed is this line, which now uses `thread2`
  run_id=run.id
)
print(run)

messages = client.beta.threads.messages.list(
  thread_id=thread2.id # The only thing that has changed is this line, which now uses `thread2`
)
print(messages)
