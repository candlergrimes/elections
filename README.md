# elections

## Objects

### `raw_polls`

Inputs:

- 538 Poll List
- My Crosstabs

### `polls`

- Add Diff row → Dem minus Rep for every category for each poll_id from `raw_polls`

### `states`

For each state and sample-wide:

- Tab: Average value for each metric
- Tab Count: Count of each metric (set a min: 3 for valid result)
- Diffs against overall state mean: tab value minus average across the state
- Diff against category mean: tab value minus sample-wide average

## Steps

1. Create State List
2. Load current 538 Polls and filter the results
    - [x]  partisan
    - [x]  fte_rating ≥ B/C
    - [x]  state list
    - [x]  likely voters

    At this point, the list is down to ~1000 polls (from ~9400). Maybe okay to leave in the really old polls in this dataset.

    - [ ]  Create date > Sep 1, 2020
3. Create a uid field (concatentate `<question_id>_<candidate_id>`)
4. Append new crosstab fields and values to polls with matching uid
5. Create `polls` object and fill with diff results from DEM and REP `candidate_party` values for each `question_id` where a crosstab result exists. 

Find a way to account for undecided/uncommitted/3rd party values to this result (i.e. Age: 30-44 is D+6 and 18% other

1. Create the `states` object  
2. Compute averages for each `state` in each crosstab where count ≥ 3
