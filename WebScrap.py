from xml.dom.minidom import TypeInfo
from bs4 import BeautifulSoup
import pip._vendor.requests as requests
#import requests
import re
import time
import os, shutil

def find_jobs():
    print('Put from which month you want to check job offers:')
    latest_month= input('>')
    print(f'Filtering out {latest_month}')
    #print(type(latest_month))

    deletefiles()

    html_text = requests.get('https://www.myjob.mu/ShowResults.aspx?Keywords=python&Location=&Category=').text
    soup = BeautifulSoup(html_text, 'lxml')

    job_list = soup.find('div', class_='two-thirds')
    jobs_content = job_list.find_all('div', class_='module-content')


    for index,job_content in enumerate(jobs_content):
    
        job = job_content.find('div', class_='job-result-title')
        job_title=job.h2.a.text   

        company_title=job.h3.a.text

        job_update = job_content.find('li', itemprop="datePosted")
        job_update=job_update.text
        
        job_close = job_content.find('li', class_='closed-time')
        job_close=job_close.text     

        more_info = job.h2.a['href']

        #print(type(job_update))
        #print(re.findall(r'\d+', job_update))
        date=re.findall(r'\d+', job_update)
        #print(type(int(date[1])))
        
        if int(date[1]) >= int(latest_month):
            with open(f'post/{index}.txt', "w") as f:
                f.write(job_title +"\n")
                f.write(company_title +"\n")
                f.write(job_update +"\n")
                f.write(job_close +"\n")
                f.write(f'More Info: https://www.myjob.mu{more_info}\n')
            print(f'File saved:{index}')
#------------------------------------------------------------
def deletefiles():
    folder = './post'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


#-------------------------------------------------------------
if __name__=='__main__':
    while True:
        find_jobs()
        time_wait = 20
        print(f'Waiting {time_wait} seconds...')
        time.sleep(time_wait*1) 

