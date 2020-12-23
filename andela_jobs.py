import requests
from bs4 import BeautifulSoup as BS
from urllib.parse import urljoin

def set_working_directory():
    import os
    if (os.path.dirname(os.path.abspath(__file__)) != os.getcwd()):
        os.chdir(os.path.dirname(os.path.abspath(__file__)))


class AndelaTechJobs:
    def __init__(self):
        self.parent_link = "https://boards.greenhouse.io/andela"
        self.page = requests.get(self.parent_link)
        self.scraper = BS(self.page.content, "html.parser")
        self.job_sections = None
        self.departments =  ['software engineering', 'technology'] 
        self.data = {} # holds information of the filtered jobs
    
    def get_scraper(self):
        return self.scraper.prettify()
    
    def find_job_sections(self):
        self.job_sections = self.scraper.find_all(class_="level-0")

    def get_job_sections(self):
        return self.job_sections
    
    def filter_jobs(self):
        filtered_jobs = []
        if self.job_sections != None:
            for each in self.job_sections:
                jobs_dept = each.select('h3')[0].get_text().lower()
                if  jobs_dept in self.departments:
                    filtered_jobs.append(each)

            return filtered_jobs
        else:
            return None
    
    def update_jobs(self):
        self.job_sections = self.filter_jobs()
    
    def extract_data(self):
        for section in self.job_sections:
            openings = section.find_all(class_="opening")
            for each in openings:
                job = each.select('a')[0].get_text()
                href = each.select('a')[0]['href']
                link = urljoin(self.parent_link, href)
                location = each.find(class_="location").get_text()
                self.data[job] = {'link': link, 'location': location}
    

    def get_data(self):
        return self.data


if __name__ ==  "__main__":
    andela_jobs = AndelaTechJobs()
    andela_jobs.find_job_sections()
    andela_jobs.update_jobs()
    andela_jobs.extract_data()
    print(andela_jobs.get_data())