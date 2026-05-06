## Final Project Proposal

### Project Title:
Medicaid Enrollment and Poverty: A Large-Scale Analysis of State-Level Trends and the Role of Medicaid Expansion
### Research Problem
Medicaid is the largest public health insurance program in the United States, yet enrollment rates vary substantially across states. 
Understanding what drives this variation — and whether state-level poverty and Medicaid expansion status explain differences in enrollment — is a central question 
in health policy research. This project investigates whether states with higher poverty rates show correspondingly higher Medicaid enrollment rates, 
and whether the ACA Medicaid expansion moderates this relationship over time.
### Data and Methods
This project integrates two large public datasets: the CMS State Medicaid and CHIP Applications, Eligibility Determinations, 
and Enrollment dataset (10,000+ monthly state-level records from 2013–2026, accessed via the CMS Open Data API) and 
the U.S. Census Bureau's American Community Survey 5-year estimates (16,000+ county-year records across 2019–2024, accessed via the Census API). 
Both datasets will be ingested programmatically and stored in Amazon S3.
Large-scale processing is necessary because the analysis requires joining two multi-year, multi-source datasets across different geographic 
granularities (state and county), computing derived metrics (poverty rate, uninsured rate, enrollment rate), and producing longitudinal comparisons 
across 50 states and 3,000+ counties. PySpark on Amazon EMR will be used for data cleaning, aggregation, and joining at scale. 
Final outputs will include state-level trend visualizations and a regression analysis of poverty rate versus enrollment rate, stratified by expansion status.
### Schedule

Week 1 (May 4–10): Data ingestion pipeline, S3 setup, initial EDA \
Week 2 (May 11–18): PySpark cleaning, joining, aggregation on EMR \
Week 3 (May 19–25): Analysis, visualization, README writeup \
May 29: Final submission

### Group: 
Individual project

### Data Source:
Medicaid and CHIP: https://data.medicaid.gov/dataset/6165f45b-ca93-5bb5-9d06-db29c692a360/data \
US Census: https://api.census.gov/data