import pandas as pd
from scipy.stats import wasserstein_distance
import seaborn as sns
import matplotlib.pyplot as plt

#puts the already done 
def bias_conversion():
    return 2

#reading human responses and saving to a dictionary --> {code:[responses],...code:[responses]}
human_df = pd.read_csv("responses/human-responses.csv")
human_responses_dict = {}
for column_header in human_df:
    human_responses_dict[column_header] = human_df[column_header].to_list()


#reading llm responses and saving to a dictionary --> 
#{approach:{questioncode:[responses],qcode:[responses]...},approach:{qcode:[responses],code:[responses]...}...}
llm_responses = {}

#union approach
nodemo_df = pd.read_csv("responses/llm/no-demos.csv")
#create dictionary of unionized demographic only responses: {code:[persona responses]}
union_responses_dict = {}
for column_header in nodemo_df:
    union_responses_dict[column_header] = nodemo_df[column_header].to_list()
##add unionized responses dict to llm responses dict as {'union':{unionresponsdict}}
llm_responses['None']=union_responses_dict

#one demographic approach
one_demo_df = pd.read_csv("responses/llm/one-demo.csv")
#create dictionary of political demographic only responses: {code:[persona responses]}
poli_responses_dict = {}
for column_header in one_demo_df:
    responses = bias_conversion()
    poli_responses_dict[column_header] = one_demo_df[column_header].to_list()
##add political responses dict to llm responses dict as {'poli':{poliresponsdict}}
llm_responses['Political']=poli_responses_dict

#repeat the same data parsing with the last approach
#intersectional approach
intersectional_df = pd.read_csv("responses/llm/intersectional.csv")
intersectional_responses_dict = {}
for column_header in intersectional_df:
    intersectional_responses_dict[column_header] = intersectional_df[column_header].to_list()
llm_responses['Political and Sex']=intersectional_responses_dict


#analyzing response similarity by question with wasserstein distance -->
# {approach:[wass-distances-by-question],...}
#creates a dictionary of list values where each list contains the distances found between llm response and human response by question
distances = {}
for approach, llm_dictionary in llm_responses.items():
    #makes a key in the distances dictionary and creates a list object as the value
    distances[approach] = []
    for code, responses in human_responses_dict.items():
        wd = wasserstein_distance(responses,llm_dictionary[code])
        distances[approach].append(wd)



#create graph with seaborn
# Convert the dictionary to a DataFrame
df = pd.DataFrame([(k, v) for k, lst in distances.items() for v in lst], columns=['Demographic Prompting', 'Distance for LLM Dataset to Become the Human Dataset'])

# Create the catplot with box type
title = "Human-Persona Similarity By Approach and Question"
sns.catplot(x='Demographic Prompting', y='Distance for LLM Dataset to Become the Human Dataset', kind='box', data=df, color='red')
plt.title(title,pad=20)
plt.tight_layout()
# Save the plot
plt.savefig('results.jpg')