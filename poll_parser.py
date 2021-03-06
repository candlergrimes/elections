import pandas as pd

pd.set_option('mode.chained_assignment',None)

state_list = ['Arizona','Wisconsin','Pennsylvania','Nevada','North Carolina','Florida','Ohio','Minnesota','Michigan','Georgia']
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

polls = polls.set_index('uid')
crosstab = crosstab.set_index('uid')
polls = polls.join(crosstab, lsuffix='_polls', rsuffix='_crosstab')
polls = polls[polls['Property'].notna()]

unique = polls.drop_duplicates(subset='question_id')
questions = unique.question_id.tolist()


diff_list = [] #container for diff dictionaries below. Will be written to the diff dataframe
undecided_list = []

for item in questions:
    dem = polls[(polls['question_id'] == item) & (polls['candidate_party'] == "DEM")]
    rep = polls[(polls['question_id'] == item) & (polls['candidate_party'] == "REP")]

    pct = dem.iloc[0]['pct'] - rep.iloc[0]['pct']
    pct_age_young = dem.iloc[0]['pct_age_young'] - rep.iloc[0]['pct_age_young']
    pct_age_mid1 = dem.iloc[0]['pct_age_mid1'] - rep.iloc[0]['pct_age_mid1']
    pct_age_mid2 = dem.iloc[0]['pct_age_mid2'] - rep.iloc[0]['pct_age_mid2']
    pct_age_old = dem.iloc[0]['pct_age_old'] - rep.iloc[0]['pct_age_old']
    pct_dem = dem.iloc[0]['pct_dem'] - rep.iloc[0]['pct_dem']
    pct_rep = dem.iloc[0]['pct_rep'] - rep.iloc[0]['pct_rep']
    pct_ind = dem.iloc[0]['pct_ind'] - rep.iloc[0]['pct_ind']
    pct_male = dem.iloc[0]['pct_male'] - rep.iloc[0]['pct_male']
    pct_fem = dem.iloc[0]['pct_fem'] - rep.iloc[0]['pct_fem']
    pct_black = dem.iloc[0]['pct_black'] - rep.iloc[0]['pct_black']
    pct_white = dem.iloc[0]['pct_white'] - rep.iloc[0]['pct_white']
    pct_hisp = dem.iloc[0]['pct_hisp'] - rep.iloc[0]['pct_hisp']
    pct_race_other = dem.iloc[0]['pct_race_other'] - rep.iloc[0]['pct_race_other']
    question_id = item
    state = dem.iloc[0]['state']


    diff_dict = {
        "question_id": question_id,
        "state": state,
        "pct_age_young": pct_age_young,
        "pct_age_mid1": pct_age_mid1,
        "pct_age_mid2": pct_age_mid2,
        "pct_age_old": pct_age_old,
        "pct_dem": pct_dem,
        "pct_rep": pct_rep,
        "pct_ind": pct_ind,
        "pct_male": pct_male,
        "pct_fem": pct_fem,
        "pct_black": pct_black,
        "pct_white": pct_white,
        "pct_hisp": pct_hisp,
        "pct_race_other": pct_race_other
        }

    diff_list.append(diff_dict)

    und = dem.iloc[0]['pct'] + rep.iloc[0]['pct']
    und_age_young = 100 - (dem.iloc[0]['pct_age_young'] + rep.iloc[0]['pct_age_young'])
    und_age_mid1 = 100 - (dem.iloc[0]['pct_age_mid1'] + rep.iloc[0]['pct_age_mid1'])
    und_age_mid2 = 100 - (dem.iloc[0]['pct_age_mid2'] + rep.iloc[0]['pct_age_mid2'])
    und_age_old = 100 - (dem.iloc[0]['pct_age_old'] + rep.iloc[0]['pct_age_old'])
    und_dem = 100 - (dem.iloc[0]['pct_dem'] + rep.iloc[0]['pct_dem'])
    und_rep = 100 - (dem.iloc[0]['pct_rep'] + rep.iloc[0]['pct_rep'])
    und_ind = 100 - (dem.iloc[0]['pct_ind'] + rep.iloc[0]['pct_ind'])
    und_male = 100 - (dem.iloc[0]['pct_male'] + rep.iloc[0]['pct_male'])
    und_fem = 100 - (dem.iloc[0]['pct_fem'] + rep.iloc[0]['pct_fem'])
    und_black = 100 - (dem.iloc[0]['pct_black'] + rep.iloc[0]['pct_black'])
    und_white = 100 - (dem.iloc[0]['pct_white'] + rep.iloc[0]['pct_white'])
    und_hisp = 100 - (dem.iloc[0]['pct_hisp'] + rep.iloc[0]['pct_hisp'])
    und_race_other = 100 - (dem.iloc[0]['pct_race_other'] + rep.iloc[0]['pct_race_other'])

    undecided_dict = {
        "question_id": question_id,
        "state": state,
        "und_age_young": und_age_young,
        "und_age_mid1": und_age_mid1,
        "und_age_mid2": und_age_mid2,
        "und_age_old": und_age_old,
        "und_dem": und_dem,
        "und_rep": und_rep,
        "und_ind": und_ind,
        "und_male": und_male,
        "und_fem": und_fem,
        "und_black": und_black,
        "und_white": und_white,
        "und_hisp": und_hisp,
        "und_race_other": und_race_other
        }

    undecided_list.append(undecided_dict)

diff = pd.DataFrame(diff_list)
undecideds = pd.DataFrame(undecided_list)
averages = pd.DataFrame()
counts = pd.DataFrame()

for i in state_list:
    state_polls_diff = diff.loc[diff['state'] == i]

    avg = state_polls_diff.mean()
    avg['state'] = i

    cnt = state_polls_diff.count()
    cnt['state'] = i

    averages = averages.append(avg, ignore_index=True)
    counts = counts.append(cnt,ignore_index=True)


averages = averages.set_index('state')
counts = counts.set_index('state')
averages = averages.join(counts,lsuffix = '_avg',rsuffix = '_cnt')
print('DIFF')
print(averages)

with open('./data/diff_output.csv','a') as diff_output:
    averages.to_csv(diff_output)

averages = pd.DataFrame()
counts = pd.DataFrame()

for i in state_list:
    state_polls_und = undecideds.loc[undecideds['state'] == i]

    avg = state_polls_und.mean()
    avg['state'] = i

    cnt = state_polls_und.count()
    cnt['state'] = i

    averages = averages.append(avg, ignore_index=True)
    counts = counts.append(cnt, ignore_index=True)

averages = averages.set_index('state')
counts = counts.set_index('state')
averages = averages.join(counts,lsuffix = '_avg',rsuffix = '_cnt')

print('UNDECIDED')
print(averages)

with open('./data/undecided_output.csv','a') as undecided_output:
    averages.to_csv(undecided_output)
