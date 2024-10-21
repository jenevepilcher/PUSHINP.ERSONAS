from openai import OpenAI
import openai
import os
import config
import pandas as pd
from humandata_cleaning import battery

# Set up OpenAI API key
api_key = config.key
openai.api_key = api_key
os.environ["OPENAI_API_KEY"] = config.key

##persona demographics and population information by aggregation level - 10% of human pop, 707 personas each approach
persona_approaches = {
                    'union': {'':707},
                    'political-only':{'who is politically moderate':155,
                            'who is conservative':128,
                            'who is liberal':106, 
                            'who hasn\'t thought much about your political leaning':101,
                            'who is slightly liberal':78,
                            'who is slightly conservative':69,
                            'who is extremely conservative':37,
                            'who is extremely liberal':31,
                            'who refuses to disclose your political leaning':2},
                    'intersectional':{'and politically moderate female':85,
                            'and politically moderate male':68,
                            'and conservative male':67,
                            'and liberal female':64, 
                            'and conservative female':60,
                            "and female who hasn't thought about your political leaning":60,
                            'and liberal male':41,
                            'and slightly liberal female':41,
                            "and male who hasn't thought about your political leaning":39,
                            'and slightly liberal male':36,
                            "and slightly conservative male":36,
                            'and slightly conservative female':33,
                            'and extremely conservative male':20, 
                            'and extremely liberal female':20,
                            "and extremely conservative female":17,
                            'and extremely liberal male':12,
                            'and political moderate who refused to disclose your sexual orientation':2,
                            'who hasn\'t thought about your political leaning and refused to disclose your sexual orientation':1, 
                            'and male who refused to disclose your political leaning':1, 
                            'and slight liberal who refused to disclose your sexual orientation':1,
                            'and conservative who refused to disclose your sexual orientation':1,
                            'and slight conservative who refused to disclose your sexual orientation':1,
                            'and male who refused to disclose your political leaning':1}
                            }



# Function to send a message to the OpenAI chatbot model and return its responses
def send_message(message_log):
    client = OpenAI()
    # Use OpenAI's ChatCompletion API to get the chatbot's response
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  
        messages=message_log,   # The conversation history up to this point, as a list of dictionaries
        max_tokens=4096,        # most amount of characters that can go in conversation
        stop=None,              # The stopping sequence for the generated response, if any (not used here)
        temperature=1.0         # The "creativity" of the generated response (higher temperature = more creative)
    ) 
    for choice in response.choices:
        if "text" in choice:
            return choice.text
    # If no response with text is found, return the first response's content (which may be empty)
    return response.choices[0].message.content



#Main function that runs the chatbot
def main(): 
    ##this loops through the approaches I take and keeps responses organized by approach
    for approach, details in persona_approaches.items():
        #collecting all responses for each approach 
        responses = {}
        ##subdemographic information of each aggregation level
        for prompt, population in details.items():
            #creates a persona for every individual in the demographic population
            for i in range(population):
                #create prompt and intro to survey
                persona_prompt = f'You are an American voter {prompt} during the 2020 presidential election. For the American National Election Survey, you are answering a series of questions about your beliefs and behaviors between August 18th, 2020 and January 4, 2021, around the 2020 presidential election. Please answer each question with only integers on the given scale most associated with your stance. No letters, words, periods, colons, semicolons, symbols, or spaces in any response please.'
                #begin survey
                for variable, information in battery.battery.items():
                    #add question to dataset and create responses list if not already there
                    if variable not in responses:
                        responses[variable]=[]
                    #create persona and ask question
                    ##persona is prompted at the same time question is asked so that the character limit is not overloaded by always appending a new question to the message log. each question starts a fresh log. no memories are stored like the human would have done, but this is the only way to automate the data without crashing midway
                    message_log = [
                    {"role": "system", "content": f'{persona_prompt}'},
                    {"role": "user", "content": f'Question: {information[0]} | Answer Choices (Please remember to answer with only the integer associated with your choice.): {information[1]}'}
                    ]
                    #send message
                    response = send_message(message_log)
                    #add response to this question to the dataset
                    responses[variable].append(response)
                    #validation that the right things are being generated
                    print(f"number: {i} | persona: {prompt} | response: {response}")
        #create dataframe of responses with variable code as the header
        df = pd.DataFrame(responses)
        #save as csv in the responses folder, same format as human responses for easy analysis
        df.to_csv(f"responses/{approach}-responses.csv", index=False)

# Call the main function if this file is executed directly (not imported as a module)
if __name__ == "__main__":
   main()