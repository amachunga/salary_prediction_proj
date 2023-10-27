import glassdoor_web_scraper as gs
import pandas as pd

path = 'C:/Users/QUEST/Documents/ds_salary_proj/chromedriver-win64/chromedriver'

df = gs.get_jobs('data scientist', 15, False, path, 3)

df