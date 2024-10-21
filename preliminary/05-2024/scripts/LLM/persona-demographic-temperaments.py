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
        max_tokens=1024,     
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
    political_leanings = ['extremely liberal', 'moderately liberal', 'slightly liberal', 'political moderate', 'slightly conservative', 'moderately conservative', 'extremely conservative']
    print("Initializing persona..") 
    all_responses = [] # list of dictionaries 
    # each dict item has the following keys: [political_leaning, question, response]
    for political_leaning in political_leanings:
        persona_description = f'You are {political_leaning}. Please answer on a scale from 0 to 100 how you feel about the given demographic in only a numerical response.Ratings between 50 degrees and 100 degrees mean that you feel favorable and warm toward the person. Ratings between 0 degrees and 50 degrees mean that you dont feel favorable toward the person and that you dont care too much for that person. You would rate the person at the 50 degree mark if you dont feel particularly warm or cold toward the person.'
        message_log = [
                {"role": "system", "content": persona_description}
            ]
        for i in range(10):
        
            #print(f"\n{political_leaning} assistant: ")
            # Initialize the conversation history with a message from the chatbot
            
            user_inputs = ['Feminists','Police','Transgender People','Conservatives','Liberals','Gay men and lesbians','Muslims','Christians','Jews','Legal Immigrants','Illegal Immigrants']
            for user_input in user_inputs:
                
                # If this is the first request, get the user's input and add it to the conversation history
                message_log.append({"role": "user", "content": user_input})

                # Send the conversation history to the chatbot and get its response
                response = send_message(message_log)

                # Add the chatbot's response to the conversation history and print it to the console
                message_log.append({"role": "assistant", "content": response})
                
                print(f"response: {response}")
                row = {"leaning": political_leaning, "demographic": user_input, "persona temperament":response}
                all_responses.append(row)

    df = pd.DataFrame.from_records(all_responses)
    df.to_csv("04112024_llm_temperaments.csv", index=False)

# Call the main function if this file is executed directly (not imported as a module)
if __name__ == "__main__":
   main()
