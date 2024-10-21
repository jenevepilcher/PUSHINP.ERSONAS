import pandas as pd
import battery

# reading csv
anes_df = pd.read_csv("humandata_cleaning/anes_timeseries_2020_csv_20220210.csv")

##getting web only
anes_df = anes_df.query('V200002 == 3')
##getting only those who completed all of pre and post surveys
anes_df = anes_df.query('V200004 == 3')

##viewing political subdemographics
political_df = anes_df['V201200']
print("POLITICAL DEMOGRAPHICS:")
print(political_df.value_counts())
print('\n\n\n')

##viewing subdemographics on intersection of political leaning and sex
intersectional_df = anes_df[['V201200','V201600']]
print("INTERSECTIONAL DEMOGRAPHICS:")
print(intersectional_df.value_counts())

##rewriting dataframe without questions that aren't in battery --> isolating battery
battery_set = []
for item in battery.battery.keys():
    battery_set.append(item)
anes_df = anes_df[battery_set]

#getting rid of -5 (interview breakoff)
negfives = {}
for key, value in anes_df.items():
    for item in value:
        if item == -5:
            negfives[key]
print(negfives)

#save to csv
anes_df.to_csv('responses/human-responses.csv',index=False)
#get out -6 -5 -4