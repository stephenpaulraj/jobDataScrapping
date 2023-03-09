from scrapDataFunctions import get_urls_within_time_range
from scrapDataFunctions import collect_job_info

# Step 1 - Get individual urls list from Jobs list
print('Running Step - 1 ....')
days_for_jobs_to_scrap = 2
individualUrlList = get_urls_within_time_range.collect_main_urls_list(days_for_jobs_to_scrap)
print('---- Step 1 - Collecting Jobs for previous ' + str(days_for_jobs_to_scrap) + ' Days. ' + 'Total URL found is '
      + str(len(individualUrlList)))

# Step 2 - Get Job and Employer Data
print('Running Step - 2 .... ')
final_data = collect_job_info.collect_company_info(individualUrlList[:2])










