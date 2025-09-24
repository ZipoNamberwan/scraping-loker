import requests
import pandas as pd
import time
from datetime import datetime


class JobScraper:
    """A class for scraping job listings from loker.id"""
    
    def __init__(self):
        """Initialize the scraper with required headers, cookies, and parameters"""
        self.cookies = {
            '_clck': 'f5c5tf%5E2%5Efzk%5E0%5E2092',
            '_ga': 'GA1.1.752074889.1758636926',
            '_gcl_au': '1.1.956823323.1758636926',
            '_ga_PF475ZB8Q5': 'GS2.1.s1758636926$o1$g1$t1758638098$j14$l0$h0',
            '_clsk': 'z07yh5%5E1758638099100%5E7%5E1%5Ey.clarity.ms%2Fcollect',
        }

        self.headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9,id;q=0.8',
            'priority': 'u=1, i',
            'referer': 'https://www.loker.id/pendidikan/sma-smk-stm/jawa-barat',
            'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Mobile Safari/537.36',
        }

        self.params = {
            '_data': 'routes/pendidikan.$education.$(location).(page).($number_page)',
        }
        
        self.base_url = 'https://www.loker.id/pendidikan/sma-smk-stm/jawa-barat/page/'
        self.delay = 0.2  # seconds between requests
        
        # Job detail API configuration
        self.detail_cookies = {
            '_ga': 'GA1.1.752074889.1758636926',
            '_gcl_au': '1.1.956823323.1758636926',
            '_clck': 'f5c5tf%5E2%5Efzl%5E0%5E2092',
            '_ga_PF475ZB8Q5': 'GS2.1.s1758721344$o2$g1$t1758724380$j51$l0$h0',
            '_clsk': 'pnpwny%5E1758725194508%5E19%5E1%5Ey.clarity.ms%2Fcollect',
        }
        
        self.detail_headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9,id;q=0.8',
            'priority': 'u=1, i',
            'referer': 'https://www.loker.id/lokasi-pekerjaan/jawa-barat',
            'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
        }
        
        self.detail_url = 'https://www.loker.id/lokasi-pekerjaan/jawa-barat'
    
    def set_delay(self, delay):
        """Set the delay between requests"""
        self.delay = delay
    
    def get_delay(self):
        """Get the current delay between requests"""
        return self.delay

    def get_single_page_jobs(self, page):
        """Get jobs from a single page"""
        url = f"{self.base_url}{page}"
        print(f"Scraping page {page}...")
        
        try:
            response = requests.get(url, params=self.params, cookies=self.cookies, headers=self.headers)
            response.raise_for_status()  # Raise an exception for bad status codes
            
            data = response.json()
            jobs = data.get('jobs', [])
            
            print(f"Found {len(jobs)} jobs on page {page}")
            return jobs
            
        except requests.exceptions.RequestException as e:
            print(f"Error on page {page}: {e}")
            return None
        except KeyError as e:
            print(f"Error parsing data on page {page}: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error on page {page}: {e}")
            return None
    
    def get_job_detail(self, job_id):
        """Get detailed information for a specific job by job ID"""
        detail_params = {
            'jobid': str(job_id),
            '_data': 'routes/lokasi-pekerjaan.$location.(page).($number_page)',
        }
        
        print(f"  Fetching details for job ID: {job_id}")
        
        try:
            response = requests.get(
                self.detail_url, 
                params=detail_params, 
                cookies=self.detail_cookies, 
                headers=self.detail_headers
            )
            response.raise_for_status()
            
            data = response.json()
            
            # Extract job detail from response (structure may vary)
            # You might need to adjust this based on the actual response structure
            if 'loaders' in data:
                for key, value in data['loaders'].items():
                    if 'JobDetailByCategory' in value:
                        return value['JobDetailByCategory']
                    elif isinstance(value, dict) and 'job' in value:
                        return value['job']
                    elif isinstance(value, dict) and value:
                        return value
            
            # If no specific structure found, return the whole data
            return data
            
        except requests.exceptions.RequestException as e:
            print(f"    Error fetching detail for job {job_id}: {e}")
            return None
        except Exception as e:
            print(f"    Unexpected error fetching detail for job {job_id}: {e}")
            return None
    
    def scrape_all_jobs(self):
        """Scrape all job listings from all pages and save to Excel"""
        all_jobs = []
        page = 1
        
        print("Starting job scraping...")
        
        while True:
            jobs = self.get_single_page_jobs(page)
            
            # Check if jobs retrieval failed or no jobs found
            if jobs is None:
                break
            
            if not jobs:
                print(f"No more jobs found on page {page}. Stopping...")
                break
            
            # Add jobs to our collection with details
            for job in jobs:
                job_id = job.get('id')
                if job_id:
                    # Fetch job details
                    job_detail = self.get_job_detail(job_id)
                    if job_detail:
                        job['detail'] = job_detail
                    
                    # Add delay between detail requests
                    time.sleep(self.delay)
                
                # Flatten nested data for better Excel representation
                flattened_job = self.flatten_job_data(job)
                all_jobs.append(flattened_job)
            
            # Delay between requests as requested
            time.sleep(self.delay)
            page += 1
        
        # Save to Excel
        if all_jobs:
            self.save_to_excel(all_jobs)
            print(f"Successfully scraped {len(all_jobs)} jobs from {page-1} pages")
        else:
            print("No jobs were scraped")
        
        return all_jobs
    
    def scrape_jobs_list_only(self):
        """Scrape only job listings without details (faster)"""
        all_jobs = []
        page = 1
        
        print("Starting job list scraping (without details)...")
        
        while True:
            jobs = self.get_single_page_jobs(page)
            
            # Check if jobs retrieval failed or no jobs found
            if jobs is None:
                break
            
            if not jobs:
                print(f"No more jobs found on page {page}. Stopping...")
                break
            
            # Add jobs to our collection without details
            for job in jobs:
                flattened_job = self.flatten_job_data(job)
                all_jobs.append(flattened_job)
            
            # Delay between requests as requested
            time.sleep(self.delay)
            page += 1
        
        # Save to Excel
        if all_jobs:
            self.save_to_excel(all_jobs)
            print(f"Successfully scraped {len(all_jobs)} jobs from {page-1} pages (list only)")
        else:
            print("No jobs were scraped")
        
        return all_jobs

    def flatten_job_data(self, job):
        """Flatten nested job data for Excel compatibility"""
        flattened = {}
        
        # Basic job information
        flattened['job_id'] = job.get('id')
        flattened['slug'] = job.get('slug')
        flattened['company_id'] = job.get('company_id')
        flattened['company_name'] = job.get('company_name')
        flattened['title'] = job.get('title')
        flattened['category'] = job.get('category')
        flattened['content'] = job.get('content')
        flattened['job_description'] = job.get('job_description')
        flattened['responsibilities'] = job.get('responsibilities')
        flattened['qualifications'] = job.get('qualifications')
        flattened['status'] = job.get('status')
        flattened['location'] = job.get('location')
        flattened['job_type'] = job.get('job_type')
        flattened['industry'] = job.get('industry')
        flattened['education'] = job.get('education')
        flattened['post_date'] = job.get('post_date')
        flattened['published_at'] = job.get('published_at')
        flattened['closed_at'] = job.get('closed_at')
        flattened['gender'] = job.get('gender')
        flattened['is_remote'] = job.get('is_remote')
        flattened['job_experience'] = job.get('job_experience')
        flattened['job_salary'] = job.get('job_salary')
        flattened['job_benefits'] = job.get('job_benefits')
        flattened['is_premium'] = job.get('is_premium')
        flattened['need_urgent'] = job.get('need_urgent')
        
        # Level information
        level = job.get('level', {})
        flattened['level_name'] = level.get('name') if level else None
        flattened['level_slug'] = level.get('slug') if level else None
        
        # Tag information
        tag = job.get('tag', {})
        flattened['tag_name'] = tag.get('name') if tag else None
        flattened['tag_slug'] = tag.get('slug') if tag else None
        
        # Salary information
        salary = job.get('salary', {})
        flattened['salary_name'] = salary.get('name') if salary else None
        flattened['salary_slug'] = salary.get('slug') if salary else None
        
        # Company information
        flattened['company_slug'] = job.get('company_slug')
        flattened['company_profile_url'] = job.get('company_profile_url')
        flattened['company_logo'] = job.get('company_logo')
        
        # Categories (join multiple categories)
        categories = job.get('categories', [])
        flattened['categories'] = '; '.join([cat.get('name', '') for cat in categories])
        
        # Locations (join multiple locations)
        locations = job.get('locations', [])
        flattened['locations'] = '; '.join([loc.get('name', '') for loc in locations])
        
        # Educations (join multiple education levels)
        educations = job.get('educations', [])
        flattened['educations'] = '; '.join([edu.get('name', '') for edu in educations])
        
        # Experiences (join multiple experience levels)
        experiences = job.get('experiences', [])
        flattened['experiences'] = '; '.join([exp.get('name', '') for exp in experiences])
        
        # Industries (join multiple industries)
        industries = job.get('industries', [])
        flattened['industries'] = '; '.join([ind.get('name', '') for ind in industries])
        
        # Job skills (join multiple skills)
        job_skills = job.get('job_skills', [])
        flattened['job_skills'] = '; '.join([skill.get('name', '') for skill in job_skills])
        
        # Types (join multiple types)
        types = job.get('types', [])
        flattened['types'] = '; '.join([typ.get('name', '') for typ in types])
        
        # Application status
        flattened['applied'] = job.get('applied')
        flattened['offered'] = job.get('offered')
        flattened['bookmarked'] = job.get('bookmarked')
        
        # Statistics
        statistic = job.get('statistic', {})
        flattened['application_count'] = statistic.get('application_count', 0)
        flattened['new_application_count'] = statistic.get('new_application_count', 0)
        flattened['hired_application_count'] = statistic.get('hired_application_count', 0)
        flattened['rejected_application_count'] = statistic.get('rejected_application_count', 0)
        
        # Job detail information (if available)
        detail = job.get('detail')
        if detail:
            flattened['detail_id'] = detail.get('id')
            flattened['detail_slug'] = detail.get('slug')
            flattened['detail_company_name'] = detail.get('company_name')
            flattened['detail_title'] = detail.get('title')
            flattened['detail_category'] = detail.get('category')
            flattened['detail_content'] = detail.get('content')
            flattened['detail_job_description'] = detail.get('job_description')
            flattened['detail_responsibilities'] = detail.get('responsibilities')
            flattened['detail_qualifications'] = detail.get('qualifications')
            flattened['detail_status'] = detail.get('status')
            flattened['detail_location'] = detail.get('location')
            flattened['detail_job_type'] = detail.get('job_type')
            flattened['detail_industry'] = detail.get('industry')
            flattened['detail_education'] = detail.get('education')
            flattened['detail_post_date'] = detail.get('post_date')
            flattened['detail_published_at'] = detail.get('published_at')
            flattened['detail_closed_at'] = detail.get('closed_at')
            flattened['detail_gender'] = detail.get('gender')
            flattened['detail_is_remote'] = detail.get('is_remote')
            flattened['detail_job_experience'] = detail.get('job_experience')
            flattened['detail_job_salary'] = detail.get('job_salary')
            flattened['detail_job_benefits'] = detail.get('job_benefits')
            flattened['detail_is_premium'] = detail.get('is_premium')
            flattened['detail_need_urgent'] = detail.get('need_urgent')
            
            # Detail categories, locations, etc.
            detail_categories = detail.get('categories', [])
            if detail_categories:
                flattened['detail_categories'] = '; '.join([cat.get('name', '') for cat in detail_categories])
            
            detail_locations = detail.get('locations', [])
            if detail_locations:
                flattened['detail_locations'] = '; '.join([loc.get('name', '') for loc in detail_locations])
            
            detail_educations = detail.get('educations', [])
            if detail_educations:
                flattened['detail_educations'] = '; '.join([edu.get('name', '') for edu in detail_educations])
            
            detail_experiences = detail.get('experiences', [])
            if detail_experiences:
                flattened['detail_experiences'] = '; '.join([exp.get('name', '') for exp in detail_experiences])
            
            detail_industries = detail.get('industries', [])
            if detail_industries:
                flattened['detail_industries'] = '; '.join([ind.get('name', '') for ind in detail_industries])
            
            detail_job_skills = detail.get('job_skills', [])
            if detail_job_skills:
                flattened['detail_job_skills'] = '; '.join([skill.get('name', '') for skill in detail_job_skills])
            
            detail_types = detail.get('types', [])
            if detail_types:
                flattened['detail_types'] = '; '.join([typ.get('name', '') for typ in detail_types])
        
        return flattened

    def save_to_excel(self, jobs_data):
        """Save jobs data to Excel file"""
        df = pd.DataFrame(jobs_data)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"loker_jobs_{timestamp}.xlsx"
        
        try:
            # Save to Excel with formatting
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Jobs', index=False)
                
                # Get the workbook and worksheet
                workbook = writer.book
                worksheet = writer.sheets['Jobs']
                
                # Auto-adjust column widths
                for column in worksheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    adjusted_width = min(max_length + 2, 50)  # Max width of 50
                    worksheet.column_dimensions[column_letter].width = adjusted_width
            
            print(f"Data saved to {filename}")
            
        except Exception as e:
            print(f"Error saving to Excel: {e}")
            # Fallback to CSV
            csv_filename = f"loker_jobs_{timestamp}.csv"
            df.to_csv(csv_filename, index=False)
            print(f"Fallback: Data saved to {csv_filename}")

# Run the scraper
if __name__ == "__main__":
    scraper = JobScraper()
    
    # Choose scraping method:
    # Option 1: Scrape with job details (slower but more comprehensive)
    print("Starting comprehensive scraping with job details...")
    scraper.scrape_all_jobs()
    
    # Option 2: Uncomment this line if you want only job lists (faster)
    # scraper.scrape_jobs_list_only()
