#Installing the required modules

from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

def get_jobs(keyword, num_jobs, verbose, path, slp_time):
    
    '''Gathers jobs as a dataframe, scraped from Glassdoor'''
    
    #Initializing the webdriver
    options = webdriver.ChromeOptions()
    
    driver = webdriver.Chrome(options=options)
    
    #Uncomment the line below if you'd like to scrape without a new Chrome window every time.
    #options.add_argument('headless')
   
    driver.set_window_size(1120, 1000)
    
    url = 'https://www.glassdoor.fr/Emploi/emplois.htm?sc.occupationParam="'+ keyword +'"&sc.locationSeoString=France&locId=86&locT=N'
    driver.get(url)
    jobs = []

    while len(jobs) < num_jobs:  #If true, should be still looking for new jobs.

        #Setting my sleep time based on internet speed
        time.sleep(slp_time)

        #Getting rid of the cookies pop up window
        try:
            reject_button = driver.find_element(By.ID, "onetrust-reject-all-handler")
            reject_button.click()
        except NoSuchElementException:
            pass
        time.sleep(.1)

        #Going through each job on the page
        job_buttons = driver.find_elements(By.CLASS_NAME, 'JobCard_jobCardWrapper__RfkFI')  #jl for Job Listing. These are the buttons we're going to click.
        for job_button in job_buttons:  

            print("Progress: {}".format("" + str(len(jobs)) + "/" + str(num_jobs)))
            if len(jobs) >= num_jobs:
                break

            job_button.click()  #You might 
            time.sleep(1)
            collected_successfully = False
            
            while not collected_successfully:
                try:
                    company_name = driver.find_element(By.CLASS_NAME, 'JobDetails_jobDetailsHeader__qKuvs').text
                    location = driver.find_element(By.XPATH, '//*[@id="job-location-1008241319458"]').text
                    job_title = driver.find_element(By.CLASS_NAME, 'JobDetails_jobTitle__Rw_gn').text
                    collected_successfully = True
                except:
                    time.sleep(5)

            try:
                salary_estimate = driver.find_element(By.CLASS_NAME, 'SalaryEstimate_averageEstimate__xF_7h').text
            except NoSuchElementException:
                salary_estimate = -1 #You need to set a "not found value. It's important."
            
            try:
                rating = driver.find_element(By.CLASS_NAME, 'EmployerProfile_employerRating__lq_ZL').text
            except NoSuchElementException:
                rating = -1 #You need to set a "not found value. It's important."

            #Printing for debugging
            if verbose:
                print("Job Title: {}".format(job_title))
                print("Salary Estimate: {}".format(salary_estimate))
                print("Rating: {}".format(rating))
                print("Company Name: {}".format(company_name))
                print("Location: {}".format(location))

            #Closing sign-up window
            try:
                driver.find_element(By.CLASS_NAME, 'CloseButton').click()
            except:
                time.sleep(.1)
            
            #Going to the Company tab
            try:
                driver.find_element(By.XPATH, '//*[@id="app-navigation"]/div[3]/div[2]/div[2]/div/section/section[2]').click()
                
                
                try:
                    size = driver.find_element(By.XPATH, '//*[@id="app-navigation"]/div[3]/div[2]/div[2]/div/section/section[2]/div/div[1]/div').text
                except NoSuchElementException:
                    size = -1

                try:
                    founded = driver.find_element(By.XPATH, '//*[@id="app-navigation"]/div[3]/div[2]/div[2]/div/section/section[2]/div/div[2]').text
                except NoSuchElementException:
                    founded = -1

                try:
                    type_of_ownership = driver.find_element(By.XPATH, '//*[@id="app-navigation"]/div[3]/div[2]/div[2]/div/section/section[2]/div/div[3]/div').text
                except NoSuchElementException:
                    type_of_ownership = -1

                try:
                    industry = driver.find_element(By.XPATH, '//*[@id="app-navigation"]/div[3]/div[2]/div[2]/div/section/section[2]/div/div[4]/div').text
                except NoSuchElementException:
                    industry = -1

                try:
                    sector = driver.find_element(By.XPATH, '//*[@id="app-navigation"]/div[3]/div[2]/div[2]/div/section/section[2]/div/div[5]/div').text
                except NoSuchElementException:
                    sector = -1

                try:
                    revenue = driver.find_element(By.XPATH, '//*[@id="app-navigation"]/div[3]/div[2]/div[2]/div/section/section[2]/div/div[6]/div').text
                except NoSuchElementException:
                    revenue = -1
                    
                    print("Success")

            except NoSuchElementException:  #Rarely, some job postings do not have the "Company" tab.

                size = -1
                founded = -1
                type_of_ownership = -1
                industry = -1
                sector = -1
                revenue = -1
                
                print("Fail")
            

            if verbose:
                print("Size: {}".format(size))
                print("Founded: {}".format(founded))
                print("Type of Ownership: {}".format(type_of_ownership))
                print("Industry: {}".format(industry))
                print("Sector: {}".format(sector))
                print("Revenue: {}".format(revenue))
                print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

            jobs.append({"Job Title" : job_title,
            "Salary Estimate" : salary_estimate,
            "Rating" : rating,
            "Company Name" : company_name,
            "Location" : location,
            "Size" : size,
            "Founded" : founded,
            "Type of ownership" : type_of_ownership,
            "Industry" : industry,
            "Sector" : sector,
            "Revenue" : revenue})
            #add job to jobs

        #Clicking on the "next page" button
        try:
            driver.find_element(By.CLASS_NAME,"button_Button__meEg5 button-base_Button__9SPjH").click()
        except NoSuchElementException:
            print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_jobs, len(jobs)))
            break

    return pd.DataFrame(jobs)  #This line converts the dictionary object into a pandas DataFrame.

