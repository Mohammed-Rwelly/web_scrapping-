from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
import time
import pandas as pd

def get_jobs(keyword, num_jobs, verbose,path):
    
    '''Gathers jobs as a dataframe, scraped from Glassdoor'''
    
    # Initializing the webdriver
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(executable_path=path, options=options)
    driver.set_window_size(1120, 1000)
    url = "https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword="+keyword+"&sc.keyword="+keyword+"&locT=&locId=&jobType="
    driver.get(url)
    # Define a global variable so even if error happens the progress can still be saved
    global jobs
    jobs = []

    # Let the page load. Change this number based on your internet speed.
    # Maybe add extra sleeping at the steps you need for more loading time. 
    time.sleep(5)

    # Click on the first job & Test for the "Sign Up" prompt and get rid of it.
    driver.find_element_by_xpath("//*[@id='MainCol']/div[1]/ul/li[1]").click()

    time.sleep(5)
    
    # Clicking on the Close X button to close the "Sign Up" prompt.
    driver.find_element_by_xpath('//*[@id="JAModal"]/div/div[2]/span').click()  
    time.sleep(5)
    while len(jobs) < num_jobs:
        
        # Going through each job in this page
        job_buttons = driver.find_elements_by_xpath("//*[@id='MainCol']/div[1]/ul/li")
        number_of_all_page=driver.find_element_by_class_name("paginationFooter").text
        print("Now we in {} ".format(number_of_all_page))
        for job_button in job_buttons:  
            print("Progress: {}".format("" + str(len(jobs)) + "/" + str(num_jobs)))
            if len(jobs) >= num_jobs:
                # When the number of jobs collected has reached the number we set. 
                break
            job_button.click()  
            time.sleep(2)
            collected_successfully = False
            
            while not collected_successfully:
                try:
                    time.sleep(5)
                    company_name = driver.find_element_by_xpath('//div[@class="css-xuk5ye e1tk4kwz5"]').text
                    location = driver.find_element_by_xpath('.//div[@class="css-56kyx5 e1tk4kwz1"]').text
                    job_title = driver.find_element_by_xpath('.//div[@class="css-1j389vi e1tk4kwz2"]').text
                    job_description = driver.find_element_by_xpath('.//div[@class="jobDescriptionContent desc"]').text
                    collected_successfully = True
                except:
                    collected_successfully = True
            try:
                salary_estimate = driver.find_element_by_xpath('//*[@id="JDCol"]/div/article/div/div[1]/div/div/div[1]/div[3]/div[1]/div[4]/span').text
            except NoSuchElementException:
                # You need to set a "not found value. It's important."
                salary_estimate = -1 
            
            try:
                rating = driver.find_element_by_xpath('//*[@id="JDCol"]/div/article/div/div[1]/div/div/div[1]/div[3]/div[1]/div[1]/span').text
            except NoSuchElementException:
                # You need to set a "not found value. It's important."
                rating = -1 

            #Printing for debugging
            if verbose:
                print("Job Title: {}".format(job_title))
                print("Salary Estimate: {}".format(salary_estimate))
                print("Job Description: {}".format(job_description))
                print("Rating: {}".format(rating))
                print("Company Name: {}".format(company_name))
                print("Location: {}".format(location))

            #Going to the Company Overflow which clicking on this these contains Size, Type , Sector ,Founded ,Industry,Revenue
            time.sleep(2)
            try:
                driver.find_element_by_xpath('.//h2[@class="mb-std css-qwgulo e9b8rvy0"]').click()
                time.sleep(2)

                try:
                    size=driver.find_element_by_xpath('//div[@class="d-flex justify-content-start css-daag8o e1pvx6aw2"]//span[text()="Size"]//following-sibling::*').text
                except NoSuchElementException:
                    size = -1

                try:
                    founded=driver.find_element_by_xpath('//div[@class="d-flex justify-content-start css-daag8o e1pvx6aw2"]//span[text()="Founded"]//following-sibling::*').text
                except NoSuchElementException:
                    founded = -1

                try:
                    type_of_ownership=driver.find_element_by_xpath('//div[@class="d-flex justify-content-start css-daag8o e1pvx6aw2"]//span[text()="Type"]//following-sibling::*').text
                except NoSuchElementException:
                    type_of_ownership = -1

                try:
                   industry=driver.find_element_by_xpath('//div[@class="d-flex justify-content-start css-daag8o e1pvx6aw2"]//span[text()="Industry"]//following-sibling::*').text
                except NoSuchElementException:
                    industry = -1

                try:
                    sector=driver.find_element_by_xpath('//div[@class="d-flex justify-content-start css-daag8o e1pvx6aw2"]//span[text()="Sector"]//following-sibling::*').text
                except NoSuchElementException:
                    sector = -1

                try:
                    revenue=driver.find_element_by_xpath('//div[@class="d-flex justify-content-start css-daag8o e1pvx6aw2"]//span[text()="Revenue"]//following-sibling::*').text
                except NoSuchElementException:
                    revenue = -1
            # Rarely, some job postings do not have the "Company" tab.
            except NoSuchElementException:  
                
                size = -1
                founded = -1
                type_of_ownership = -1
                industry = -1
                sector = -1
                revenue = -1
                             
            if verbose:
                
                print("Size: {}".format(size))
                print("Founded: {}".format(founded))
                print("Type of Ownership: {}".format(type_of_ownership))
                print("Industry: {}".format(industry))
                print("Sector: {}".format(sector))
                print("Revenue: {}".format(revenue))
                

            jobs.append({
            "Job Title" : job_title,
            "Salary Estimate" : salary_estimate,
            "Job Description" : job_description,
            "Rating" : rating,
            "Company Name" : company_name,
            "Location" : location,
            "Size" : size,
            "Company Founded Date" : founded,
            "Type of ownership" : type_of_ownership,
            "Industry" : industry,
            "Sector" : sector,
            "Revenue" : revenue
            })

        # Clicking on the "next page" button
        try:
            driver.find_element_by_css_selector('[alt="next-icon"]').click()
            time.sleep(2)
        except NoSuchElementException:
            print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_jobs, len(jobs)))
            break
            
    #This line converts the dictionary object into a pandas DataFrame.
    return pd.DataFrame(jobs)
path='chromedriver.exe'  
df=get_jobs('data scientist',1000, False,path)
df.to_csv("data_from_glassdoor.csv",index=False)