# untuk menjalankan browser yang biasa kita pakai, paste kode berikut ke command prompt. pastika port 9222 kosong dan tidak digunakan proses lain.
# "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --remote-debugging-port=9222 --user-data-dir="C:\edge-dev-profile"
# "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --profile-directory="Profile 6"

from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import os
import time
import pandas as pd
from datetime import datetime

def connect_to_existing_edge(debug=True):
    edge_options = Options()
    edge_options.add_experimental_option("debuggerAddress", "localhost:9222")
    
    # Use your downloaded EdgeDriver version 140
    service = Service("msedgedriver.exe")  # Make sure this file is in same folder
    driver = webdriver.Edge(service=service, options=edge_options)

    # Base URL without page parameter
    base_url = "https://glints.com/id/opportunities/jobs/explore?country=ID&locationId=06c9e480-42e7-4f11-9d6c-67ad64ccc0f6&locationName=Jawa+Barat&lowestLocationLevel=2&educationLevel=HIGH_SCHOOL"
    
    # Debug parameter: limit pages based on debug mode
    max_pages = 2 if debug else 33
    mode = "DEBUG MODE (2 pages only)" if debug else "FULL MODE (33 pages)"
    print(f"Starting job scraping... {mode}")
    
    # Array to store all job links
    all_job_links = []
    
    # Loop through pages
    for page_num in range(1, max_pages + 1):
        print(f"\n=== Processing Page {page_num}/{max_pages} ===")
        
        # Construct URL for current page
        current_url = f"{base_url}&page={page_num}"
        print(f"Loading: {current_url}")
        
        # Navigate to the page
        driver.get(current_url)
        
        # Wait for page to load
        time.sleep(3)
        
        # Extract job links from this page
        try:
            page_job_links = extract_job_links(driver, page_num)
            all_job_links.extend(page_job_links)
        except Exception as e:
            print(f"Error processing page {page_num}: {e}")
        
        # Add delay between pages (optional)
        time.sleep(2)
    
    # Print results
    print(f"\n=== RESULTS ===")
    print(f"Total job links found: {len(all_job_links)}")
    print("\nAll job links:")
    for i, link in enumerate(all_job_links, 1):
        print(f"{i:3d}. {link}")
    
    # Now loop through each job link and extract detailed information
    all_job_data = []
    
    if all_job_links:
        print(f"\n=== EXTRACTING JOB DETAILS FROM EACH LINK ===")
        for i, job_link in enumerate(all_job_links, 1):
            print(f"\n--- Processing Job {i}/{len(all_job_links)} ---")
            print(f"URL: {job_link}")
            
            try:
                # Navigate to the job page
                driver.get(job_link)
                
                # Wait for page to load
                time.sleep(3)
                
                # Extract job details
                job_data = extract_job_details(driver, job_link)
                
                if job_data:
                    all_job_data.append(job_data)
                    print(f"✓ Successfully extracted data for: {job_data.get('job_title', 'Unknown')}")
                else:
                    print(f"✗ Failed to extract data from job {i}")
                
                # Optional: Add delay between job visits
                time.sleep(2)
                
            except Exception as e:
                print(f"✗ Error processing job {i}: {e}")
        
        print(f"\n=== Finished processing all {len(all_job_links)} job links ===")
        
        # Save to Excel
        if all_job_data:
            save_to_excel(all_job_data, debug)
        else:
            print("No job data extracted to save.")
    else:
        print("\nNo job links found to process.")
    
    print(f"\n=== Finished processing all {max_pages} pages ===")
    input("Press Enter to quit...")
    driver.quit()
    
    return all_job_links

def extract_job_links(driver, page_num):
    """
    Extract job links from the current page
    Returns array of job links (href attributes)
    """
    job_links = []
    
    try:
        # Find the job list container
        job_list_container = driver.find_element(By.CSS_SELECTOR, 
            'div[class*="CompactJobCardListsc__JobCardListContainer"]')
        
        # Find all job cards within the container
        job_cards = job_list_container.find_elements(By.CSS_SELECTOR, 
            'div[class*="JobCardsc__JobcardContainer"]')
        
        print(f"Found {len(job_cards)} job cards on page {page_num}")
        
        # Extract link from each job card
        for i, card in enumerate(job_cards):
            try:
                # Look for the job title link within each card
                # The link is in the h2 > a structure
                job_link_element = card.find_element(By.CSS_SELECTOR, 
                    'h2[class*="CompactOpportunityCardsc__JobTitle"] a')
                
                # Get the href attribute
                job_href = job_link_element.get_attribute('href')
                
                if job_href:
                    # Convert relative URL to absolute if needed
                    if job_href.startswith('/'):
                        job_href = 'https://glints.com' + job_href
                    
                    job_links.append(job_href)
                    print(f"  Card {i+1}: {job_href}")
                else:
                    print(f"  Card {i+1}: No href found")
                    
            except Exception as e:
                print(f"  Card {i+1}: Error extracting link - {e}")
                
    except Exception as e:
        print(f"Error finding job cards on page {page_num}: {e}")
    
    return job_links

def extract_job_details(driver, job_url):
    """
    Extract detailed job information from individual job page
    Returns dictionary with job details
    """
    job_data = {
        'url': job_url,
        'job_title': '',
        'salary': '',
        'location': '',
        'education_requirement': '',
        'experience_requirement': '',
        'required_skills': '',
        'job_description': ''
    }
    
    try:
        # 1. Extract Job Title
        try:
            job_title_element = driver.find_element(By.CSS_SELECTOR, 
                'h1[class*="TopFoldExperimentsc__JobOverViewTitle"]')
            job_data['job_title'] = job_title_element.text.strip()
        except NoSuchElementException:
            job_data['job_title'] = "Not found"
        
        # 2. Extract Salary
        try:
            salary_element = driver.find_element(By.CSS_SELECTOR, 
                'span[class*="TopFoldExperimentsc__BasicSalary"]')
            job_data['salary'] = salary_element.text.strip()
        except NoSuchElementException:
            job_data['salary'] = "Not found"
        
        # 3. Extract Location from Breadcrumbs (regency after Jawa Barat)
        try:
            # Find all breadcrumb links
            breadcrumb_links = driver.find_elements(By.CSS_SELECTOR, 
                'div[class*="Breadcrumbsc__BreadcrumbInner"] a[class*="Breadcrumbsc__BreadcrumbJobLink"]')
            
            # Look for "Jawa Barat" and get the next location
            jawa_barat_found = False
            for i, link in enumerate(breadcrumb_links):
                link_text = link.text.strip()
                if jawa_barat_found and link_text:
                    # This is the location after Jawa Barat
                    job_data['location'] = link_text
                    break
                elif "jawa barat" in link_text.lower() or "jawa-barat" in link.get_attribute('href').lower():
                    jawa_barat_found = True
            
            if not job_data['location']:
                job_data['location'] = "Not found"
        except Exception:
            job_data['location'] = "Not found"
        
        # 4. Extract Education Requirement (after graduation hat icon)
        try:
            # Look for the graduation hat SVG and get the next element
            education_elements = driver.find_elements(By.XPATH, 
                '//svg[contains(@class, "CardJobEducationLevel__GraduationHatIcon")]/following-sibling::span')
            if education_elements:
                job_data['education_requirement'] = education_elements[0].text.strip()
            else:
                job_data['education_requirement'] = "Not found"
        except Exception:
            job_data['education_requirement'] = "Not found"
        
        # 5. Extract Experience Requirement (after briefcase icon)
        try:
            # Look for experience info in job overview sections
            job_info_sections = driver.find_elements(By.CSS_SELECTOR, 
                'div[class*="TopFoldExperimentsc__JobOverViewInfo"]')
            for section in job_info_sections:
                text = section.text.strip()
                if 'tahun pengalaman' in text or 'pengalaman' in text:
                    job_data['experience_requirement'] = text
                    break
            if not job_data['experience_requirement']:
                job_data['experience_requirement'] = "Not found"
        except Exception:
            job_data['experience_requirement'] = "Not found"
        
        # 6. Extract Required Skills
        try:
            skills_container = driver.find_element(By.CSS_SELECTOR, 
                'div[class*="Skillssc__TagContainer"]')
            skill_elements = skills_container.find_elements(By.CSS_SELECTOR, 
                'p[class*="Skillssc__TagName"]')
            skills = [skill.text.strip() for skill in skill_elements if skill.text.strip()]
            job_data['required_skills'] = ' | '.join(skills) if skills else "Not found"
        except NoSuchElementException:
            job_data['required_skills'] = "Not found"
        
        # 7. Extract Job Description
        try:
            job_desc_container = driver.find_element(By.CSS_SELECTOR, 
                'div[aria-label="Job Description"][class*="Opportunitysc__JobDescriptionContainer"]')
            
            # Get all text from the description container, excluding the title
            description_text_elements = job_desc_container.find_elements(By.CSS_SELECTOR, 
                'div[class*="DraftjsReadersc__ContentContainer"] li, div[class*="DraftjsReadersc__ContentContainer"] p')
            
            description_parts = []
            for element in description_text_elements:
                text = element.text.strip()
                if text and text not in description_parts:
                    description_parts.append(text)
            
            job_data['job_description'] = ' | '.join(description_parts) if description_parts else "Not found"
        except NoSuchElementException:
            job_data['job_description'] = "Not found"
        
        return job_data
        
    except Exception as e:
        print(f"Error extracting job details: {e}")
        return None

def save_to_excel(job_data_list, debug_mode):
    """
    Save job data to Excel file
    """
    try:
        # Create DataFrame
        df = pd.DataFrame(job_data_list)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        mode_suffix = "_debug" if debug_mode else "_full"
        filename = f"glints_jobs{mode_suffix}_{timestamp}.xlsx"
        
        # Save to Excel
        df.to_excel(filename, index=False, sheet_name='Jobs')
        
        print(f"\n=== EXCEL FILE SAVED ===")
        print(f"Filename: {filename}")
        print(f"Total jobs saved: {len(job_data_list)}")
        print(f"Columns: {list(df.columns)}")
        
        # Display summary
        print(f"\n=== SUMMARY ===")
        for i, job in enumerate(job_data_list, 1):
            print(f"{i:3d}. {job.get('job_title', 'N/A')} - {job.get('salary', 'N/A')}")
        
    except Exception as e:
        print(f"Error saving to Excel: {e}")
        print("Attempting to save as CSV instead...")
        try:
            df = pd.DataFrame(job_data_list)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            mode_suffix = "_debug" if debug_mode else "_full"
            filename = f"glints_jobs{mode_suffix}_{timestamp}.csv"
            df.to_csv(filename, index=False)
            print(f"Successfully saved as CSV: {filename}")
        except Exception as csv_error:
            print(f"Failed to save CSV as well: {csv_error}")

if __name__ == "__main__":
    # Set debug=True for testing (2 pages only)
    # Set debug=False for production (33 pages)
    connect_to_existing_edge(debug=False)  # Change to False for full scraping