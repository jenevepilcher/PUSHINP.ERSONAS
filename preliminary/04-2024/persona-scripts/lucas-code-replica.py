## uncommented code is lucas's with small changes to mimic republican
## commented code is early attempts to make more assistant/personas, running congruently
## plan on making less redundant by putting each section (thread creation, assistant creation, runs, etc.) through for loops (for i in range(len(data)) 
## will also help prepare code to have ANES data input for future
## error is timeout - infinite loop. stays on "waiting for assistant....". line 101 shows that the run fails.


from openai import OpenAI
import os
import config
import openai
import time

client = OpenAI(api_key=config.Items.key)

# os.environ["OPENAI_API_KEY"] = config.Items.key
# Set up OpenAI API key
api_key = config.Items.key
#openai.api_key = api_key


#creating assistants. each assistant has their own persona
# democrat = client.beta.assistants.create(
#     name="Democrat",
#     instructions="You are an extreme democrat. Answer questions as if you are a democrat",
#     tools=[{"type": "code_interpreter"}],
#     model="gpt-3.5-turbo-1106"
# )

republican = client.beta.assistants.create(
   name="Republican",
   instructions="You are an extreme republican. You are pro gun rights. Answer the user's questions as if you are a republican",
   #tools=[{"type": "code_interpreter"}],
   model="gpt-3.5-turbo-1106"
)

# independent = client.beta.assistants.create(
#    name="Republican",
#    instructions="You have no political stance. Your opinion is against the two party system. Answer questions as if this is the case.",
#    tools=[{"type": "code_interpreter"}],
#    model="gpt-3.5-turbo-1106"
# )


#creating threads for each persona
# democrat_thread = client.beta.threads.create()
republican_thread = client.beta.threads.create()
# independent_thread = client.beta.threads.create()



#asking republican, democrat, and independent about gun rights opinion
# independent_message = client.beta.threads.messages.create(
#     thread_id=independent_thread.id,
#     role="user",
#     content="What do you think about gun rights?"
# )

republican_message = client.beta.threads.messages.create(
    thread_id=republican_thread.id,
    role="user",
    content="What do you think about gun rights?"
)

# democrat_message = client.beta.threads.messages.create(
#     thread_id=democrat_thread.id,
#     role="user",
#     content="What do you think about gun rights?"
# )



# democrat_run = client.beta.threads.runs.create(
#   thread_id=democrat_thread.id,
#   assistant_id=democrat.id,
# )

republican_run = client.beta.threads.runs.create(
  thread_id=republican_thread.id,
  assistant_id=republican.id,
  instructions='You are a republican and believe in gun rights. Answer in this way.'
)


# independent_run = client.beta.threads.runs.create(
#   thread_id=independent_thread.id,
#   assistant_id=independent.id,
# )



while True:
    # waiting 2 seconds
    time.sleep(2)

    # retrieving the messages
    run_status = client.beta.threads.runs.retrieve(
        thread_id=republican_thread.id,
        run_id=republican_run.id
    )
    print(run_status.status) ##prints 'failed'
    if run_status.status == 'completed':
        messages = client.beta.threads.messages.list(
        thread_id=republican_thread.id
    )

    #displaying the messages
        for message in reversed(messages.data):
            print(f"{message.role}: {message.content[0].text.value}")
        break
    else:
        print("Waiting for the Assistant...")
        time.sleep(2)
