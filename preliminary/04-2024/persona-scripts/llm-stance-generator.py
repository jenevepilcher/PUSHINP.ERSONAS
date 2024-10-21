from openai import OpenAI
import openai
import os
import config
import pandas as pd

# Set up OpenAI API key
os.environ["OPENAI_API_KEY"] = config.Items.key
openai.api_key = config.Items.key


# Function to send a message to the OpenAI chatbot model and return its response
def send_message(message_log):
    client = OpenAI() ##dont know exactly what this means still
    # Use OpenAI's ChatCompletion API to get the chatbot's response
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  
        messages=message_log,   # The conversation history up to this point, as a list of dictionaries
        max_tokens=80,     
        temperature=0.0,        # The "creativity" of the generated response (higher temperature = more creative)
    )  ##^^^what does this mean by 'creativity'
    # if theres text in the 
    for choice in response.choices:
        if "text" in choice:
            return choice.text
    # If no response with text is found, return the first response's content (which may be empty)
    return response.choices[0].message.content


# Main function that runs the chatbot
def main():
    political_leanings = ['extreme republican', 'moderate republican', 'slightly republican', 'independent constituent', 'slightly democrat', 'moderate democrat', 'extreme democrat']
    print("Initializing personas..") 
    # all_responses will be passed to pd.DataFrame.from_records(), where each key is a column name, and each k-v pair is a row in the df 
    all_responses = [] # list of dictionaries 
    # each dict item has the following keys: [political_leaning, question, response]
    for political_leaning in political_leanings:
        print(f"\n{political_leaning} assistant: ")
        # Initialize the conversation history with a message from the chatbot
        persona_description = f'You are a {political_leaning}, answering a serious of questions regarding your political beliefs. Please answer each question, first, with a number on the given scale most associated with your stance, then, with any other needed commentary to support your belief.'
        message_log = [
            {"role": "system", "content": persona_description}
        ]
        user_inputs = ['There has been some discussion about abortion during recent years. Which one of the opinions on this page best agrees with your view? 1. By law, abortion should never be permitted. 2. The law should permit abortion only in case of rape, incest, or when the woman life is in danger. 3. The law should permit abortion for reasons other than rape, incest, or danger to the womans life, but only after the need for the abortion has been clearly established. 4. By law, a woman should always be able to obtain an abortion as a matter of personal choice.',
                        'Do you think the federal government should make it more difficult for people to buy a gun than it is now, make it easier for people to buy a gun, or keep these rules about the same as they are now? 1. More difficult 2. Easier 3. Keep these rules about the same',
                        'Do you think that people in government waste a lot of the money we pay in taxes, waste some of it, or dont waste very much of it? 1. Waste a lot 2. Waste some 3. Dont waste very much',
                        'Are we spending too much, too little, or about the right amount on health? 1. Too much 2. Too little 3. About the right amount',
                        'What is the best way to deal with the problem of urban unrest and rioting? Some say it is more important to use all available force to maintain law and order, no matter what results. Others say it is more important to correct the problems of racism and police violence that give rise to the disturbances. And, of course, other people have opinions in between. On this scale from 1 to 7, where 1 means solve problems of racism and police violence, and 7 means use all available force to maintain law and order, where would you place yourself on this scale? Here is your scale of possible answers again: \n1. Solve problems of racism and police violence \n2. \n3. \n4. \n5. \n6. \n7. Use all available force to maintain law and order',
                        'Where would you place yourself on this scale? \n1. Government should provide many fewer services \n2. \n3. \n4. \n5. \n6. \n7. Government should provide many more services',
                        'Do you favor an increase, decrease, or no change in government spending to help people pay for health insurance when people can’t pay for it all themselves? 1. Increase 2. Decrease 3. No change'	
                        ]
        for user_input in user_inputs:
            
            # If this is the first request, get the user's input and add it to the conversation history
            message_log.append({"role": "user", "content": user_input})

            # Send the conversation history to the chatbot and get its response
            response = send_message(message_log)

            # Add the chatbot's response to the conversation history and print it to the console
            message_log.append({"role": "assistant", "content": response})
            
            print(f"{political_leaning} response: {response}")
            row = {"political_leaning": political_leaning,"question": user_input, "response":response}
            all_responses.append(row)

    df = pd.DataFrame.from_records(all_responses)
    print(df.head())
    df.to_parquet("04032024_stances.parquet")
    df.to_csv("04032024_stances.csv", index=False)

# Call the main function if this file is executed directly (not imported as a module)
if __name__ == "__main__":
   main()
