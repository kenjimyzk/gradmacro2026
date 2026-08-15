# U.S. real GDP data for Lecture 2

- File: `gdpc1.csv`
- Series: Real Gross Domestic Product (`GDPC1`)
- Source: U.S. Bureau of Economic Analysis via FRED
- Frequency: quarterly
- Units: billions of chained 2017 dollars, seasonally adjusted annual rate
- Download URL: <https://fred.stlouisfed.org/graph/fredgraph.csv?id=GDPC1>
- Retrieved: 2026-08-15
- Observations in this snapshot: 1947Q1--2026Q2
- SHA-256: `f7cfe97b773eef3bd354aa722fd632bcae10b30f43e5aefcc3de89b5e251c346`

The series is revised by the source. Keeping this dated snapshot makes the rendered
lecture figure reproducible. Refresh the CSV deliberately, update the retrieval date
and checksum above, then rerun:

```sh
python3 scripts/lecture02/generate_us_real_gdp_hp.py
```
