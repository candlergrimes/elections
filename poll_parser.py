import pandas as pd

pd.set_option('mode.chained_assignment',None)

state_list = ['Arizona','Wisconsin','Pennsylvania','Nevada','North Carolina','Florida','Ohio','Minnesota','Michigan']
fte_list = ['A','A-','A/B','A+','B','B-','B/C','B+']

polls_fh = open('./data/president_polls.csv') # get file handle for current 538 polling data
crosstab_fh = open('./data/crosstab.csv') # get file handle for my crosstab  list

raw_polls = pd.read_csv(polls_fh)
polls_1 = raw_polls[raw_polls.partisan.isnull()] #remove partisan polls]
polls_2 = polls_1[polls_1.fte_grade.isin(fte_list)] # remove low grade pollsters
polls_3 = polls_2[polls_2.state.isin(state_list)] #isolate polls from state_list
polls = polls_3[polls_3['population']=='lv'] # get only Likely Voter polls

# CREATE UID
polls["question_id"] = polls['question_id'].astype(str)
polls["candidate_id"] = polls['candidate_id'].astype(str)
polls['uid'] = polls["question_id"].str.cat(polls["candidate_id"],sep ="_")

crosstab = pd.read_csv(crosstab_fh)

polls = polls.set_index('uid').join(crosstab.set_index('uid'), lsuffix='_polls', rsuffix='_crosstab')


with open('./data/output.csv','a') as out_file:
    polls.to_csv(out_file)
