# elections



## Inputs
- [538 Poll List](https://projects.fivethirtyeight.com/polls-page/president_polls.csv)
- Custom Crosstabs: manual data entry using the link to sources in the 538 poll CSV.

## Objects
**Data Prep:**
* `polls`: joins the 538 polls and the custom crosstabs
* `diff`: computes the party-wise advantage in each poll (DEM - REP)
* `undecided`: computes the proportion of 3rd party, undecided and refused groups (100 - (DEM + REP))
* `averages`: placeholder object used to compute mean diff + undecided values for each state. 
* `counts`: placeholder object used to compute count of crosstab values (i.e. # of results for `pct_black`) voters. Used to indicate small sample sizes.

**Outputs:**
* diff_output.csv: list of states with average party-wise advantages (and counts) for each crosstab 
* undecided_output.csv: list of states with proportions (and counts) of non-REP/DEM voters for each crosstab
    * NOTE: This includes 3rd party voters, so "undecided" isn't a great term...

