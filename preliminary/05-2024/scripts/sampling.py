import pandas as pd

# reading csvs
anes_df = pd.read_csv("/Users/jenevepilcher/llm-personas/scripts/ANES/anes_timeseries_2020_csv_20220210.csv")
llm_df = pd.read_csv("/Users/jenevepilcher/llm-personas/data/no demographics - baseline/05082024_llm_stances.csv")
stance_columns = {  ##major political disagreements
            'V201200': 'leaning',
            'V201336':'abortion',
            'V202337': 'gunrights',
            'V201235': 'taxwaste',
            'V201429': 'riotsolution',
            'V201246': 'govservices',
            'V202378': 'healthservices',
            }
anes_df.rename(columns=stance_columns, inplace=True)
#creating new dataframes of selected data
anes_stances = anes_df[list(stance_columns.values())]
#cleaning data
leaningsllm = llm_df.replace(['There has been some discussion about abortion during recent years. Which one of the opinions on this page best agrees with your view? 1. By law, abortion should never be permitted. 2. The law should permit abortion only in case of rape, incest, or when the woman life is in danger. 3. The law should permit abortion for reasons other than rape, incest, or danger to the womans life, but only after the need for the abortion has been clearly established. 4. By law, a woman should always be able to obtain an abortion as a matter of personal choice.','Do you think the federal government should make it more difficult for people to buy a gun than it is now, make it easier for people to buy a gun, or keep these rules about the same as they are now? 1. More difficult 2. Easier 3. Keep these rules about the same','Do you think that people in government waste a lot of the money we pay in taxes, waste some of it, or dont waste very much of it? 1. Waste a lot 2. Waste some 3. Dont waste very much','What is the best way to deal with the problem of urban unrest and rioting? Some say it is more important to use all available force to maintain law and order, no matter what results. Others say it is more important to correct the problems of racism and police violence that give rise to the disturbances. And, of course, other people have opinions in between. On this scale from 1 to 7, where 1 means solve problems of racism and police violence, and 7 means use all available force to maintain law and order, where would you place yourself on this scale? Here is your scale of possible answers again: \n1. Solve problems of racism and police violence \n2. \n3. \n4. \n5. \n6. \n7. Use all available force to maintain law and order','Where would you place yourself on this scale? \n1. Government should provide many fewer services \n2. \n3. \n4. \n5. \n6. \n7. Government should provide many more services','Do you favor an increase, decrease, or no change in government spending to help people pay for health insurance when people cant pay for it all themselves? 1. Increase 2. Decrease 3. No change'],["abortion",'gunrights','taxwaste','riotsolution','govservices','healthservices'])
leaningsanes = anes_stances.query('0 < leaning <= 7')
leaningsanes = leaningsanes.query('0 < abortion <= 4')
leaningsanes = leaningsanes.query('0 < gunrights <= 3')
leaningsanes = leaningsanes.query('0 < taxwaste <= 3')
leaningsanes = leaningsanes.query('0 < riotsolution <= 7')
leaningsanes = leaningsanes.query('0 < govservices <= 7')
leaningsanes = leaningsanes.query('0 < healthservices <= 3').sample(100)
# print(leaningsllm.loc[leaningsllm['question']=='abortion'].value_counts('response'))
# print(leaningsanes['abortion'].value_counts())
# print(leaningsllm.loc[leaningsllm['question']=='gunrights'].value_counts('response'))
# print(leaningsanes['gunrights'].value_counts())
# print(leaningsllm.loc[leaningsllm['question']=='taxwaste'].value_counts('response'))
# print(leaningsanes['taxwaste'].value_counts())
# print(leaningsllm.loc[leaningsllm['question']=='riotsolution'].value_counts('response'))
# print(leaningsanes['riotsolution'].value_counts())
# print(leaningsllm.loc[leaningsllm['question']=='govservices'].value_counts('response'))
# print(leaningsanes['govservices'].value_counts())
print(leaningsllm.loc[leaningsllm['question']=='healthservices'].value_counts('response'))
print(leaningsanes['healthservices'].value_counts())