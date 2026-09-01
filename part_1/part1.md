<h1> Assumptions </h1>
<h2> Validation Rules for Date, Town, Flat Type, Flat Model, and storey_range </h2>

- Ideally, we have a whitelist/enum table that maintains what flat types are available in a Town, what Flat Model are possible based on Flat Type etc
- We'll then validate for each record, whether the combination is valid - flag out if it doesn't exist and check the source of truth
- For now in the absence of this whitelist, I'll just implement a simple date format check to make sure Date follows the YYYY-MM format 

<h2> Heuristic for Flagging Anomalous Resale Prices </h2>

- Metric we track is resale_price_per_sqm, a basic attempt at normalization (bigger houses fetch higher prices)
- Criteria used to exclude is 3-sigma outliers, meaning we exclude the most extreme 0.27% of resale_price_per_sqm
- We could also apply this criteria to a subset of attributes that are known to affect resale_price_psm (eg Town, Flat Type, storey_range), but this was not done to remain more conservative and not exclude too many records without first verifying there is a statistically significant correlation with those attributes