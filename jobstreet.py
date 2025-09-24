import requests
import pandas as pd
import time
from datetime import datetime


class JobStreetScraper:
    """A class for scraping job listings from JobStreet Indonesia"""
    
    def __init__(self):
        """Initialize the scraper with required headers, cookies, and parameters"""
        self.cookies = {
            'sol_id': '5b600d91-3699-4b69-8c83-f33134983b1d',
            '_ga': 'GA1.1.1658404211.1758638743',
            '_tt_enable_cookie': '1',
            '_ttp': '01K5VGK85QX7THBQ97K9HMB7NC_.tt.1',
            '_fbp': 'fb.1.1758638743749.735183043440681538',
            'ajs_anonymous_id': 'ff7afac45048707f79632325386a217f',
            '_gcl_au': '1.1.51445185.1758638744',
            'da_cdt': 'visid_019977099112001741f2652009000506f001906700bd0-sesid_1758722117496-hbvid_5b600d91_3699_4b69_8c83_f33134983b1d-tempAcqSessionId_1758722117501-tempAcqVisitorId_5b600d9136994b698c83f33134983b1d',
            '_hjSessionUser_640499': 'eyJpZCI6IjRlOTEzM2VmLTcyOTMtNWExZi05OGJlLWQzZjE0MWQ2YjE4MiIsImNyZWF0ZWQiOjE3NTg2Mzg3NDQ0MzYsImV4aXN0aW5nIjp0cnVlfQ==',
            '_hjHasCachedUserAttributes': 'true',
            '_clck': '1h5hlup%5E2%5Efzl%5E0%5E2092',
            'da_searchTerm': 'undefined',
            '__gads': 'ID=8ad9a68cb5c684fa:T=1758638767:RT=1758722122:S=ALNI_MY4Ytzuptq1nsD4a1_X-t_eJrXyVA',
            '__gpi': 'UID=0000119a3b97aea1:T=1758638767:RT=1758722122:S=ALNI_MZuTETQTZh_ltRrwlkt6v8KFdkSiQ',
            '__eoi': 'ID=e59624fa2967b995:T=1758638767:RT=1758722122:S=AA-Afjahs8Yjg17hOIYmY_KEHh1a',
            'JobseekerSessionId': 'd3183f3b-a12e-4f65-ae9b-06136107c9b6',
            'JobseekerVisitorId': 'd3183f3b-a12e-4f65-ae9b-06136107c9b6',
            'main': 'V%7C2~P%7Cjobsearch~WH%7CJawa%20Barat~WID%7C2030700~OSF%7Cquick&set=1758722863359/V%7C2~P%7Cjobsearch~OSF%7Cquick&set=1758638939137/V%7C2~P%7Cjobsearch~WID%7C2030916~I%7C6281~OSF%7Cquick&set=1758638937615',
            '_cfuvid': 'Lm.9W4CkDj2z3drHTU5qIT4QD0umAmjNBz_qlFVYMKw-1758722863074-0.0.1.1-604800000',
            'utag_main': 'v_id:019977099112001741f2652009000506f001906700bd0$_sn:2$_se:4%3Bexp-session$_ss:0%3Bexp-session$_st:1758724664320%3Bexp-session$ses_id:1758722117496%3Bexp-session$_pn:1%3Bexp-session$_prevpage:search%20results%3Bexp-1758726464330',
            '_ga_DSKCDC8253': 'GS2.1.s1758722118$o3$g1$t1758722864$j60$l0$h0',
            'ttcsid': '1758722118833::34cNnkGvbbhawpixwlUy.2.1758722864372.0',
            '_uetsid': 'fb5f87f0988b11f09d8ca74108b00878',
            '_uetvid': 'fb5f8c50988b11f0bdd25bb2cc52092b',
            'hubble_temp_acq_session': 'id%3A1758722117501_end%3A1758725592628_sent%3A16',
            '_clsk': 'lxc2ni%5E1758739088620%5E1%5E0%5Ey.clarity.ms%2Fcollect',
            '_dd_s': 'rum=0&expire=1758740039406&logs=0',
            'ttcsid_CR8MQEJC77UC0UOHC250': '1758739139429::_EPMV9w6eKCIOorwHxQo.3.1758739139429.0',
        }

        self.headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9,id;q=0.8',
            'priority': 'u=1, i',
            'referer': 'https://id.jobstreet.com/id/jobs/in-Jawa-Barat',
            'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'seek-request-brand': 'jobstreet',
            'seek-request-country': 'ID',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
            'x-seek-checksum': '12a7c5c7',
            'x-seek-site': 'Chalice',
        }
        
        self.base_url = 'https://id.jobstreet.com/api/jobsearch/v5/search'
        self.base_params = {
            'siteKey': 'ID-Main',
            'sourcesystem': 'houston',
            'eventCaptureSessionId': 'b3425f79-1258-4f2d-8f93-c4c825e782c4',
            'userid': 'b3425f79-1258-4f2d-8f93-c4c825e782c4',
            'userqueryid': 'e273e973b2ff4be76d37749857dfb0c3-9139545',
            'usersessionid': 'b3425f79-1258-4f2d-8f93-c4c825e782c4',
            'where': 'Jawa Barat',
            'pageSize': '32',
            'include': 'seodata,gptTargeting',
            'locale': 'id-ID',
            'solId': '5b600d91-3699-4b69-8c83-f33134983b1d',
            'source': 'SEARCH_ENG',
            'facets': 'distinctTitle'
        }
        
        self.delay = 0.5  # seconds between requests
        
        # Job detail API configuration (different from job list API)
        self.detail_cookies = {
            'sol_id': '5b600d91-3699-4b69-8c83-f33134983b1d',
            '_ga': 'GA1.1.1658404211.1758638743',
            '_tt_enable_cookie': '1',
            '_ttp': '01K5VGK85QX7THBQ97K9HMB7NC_.tt.1',
            '_fbp': 'fb.1.1758638743749.735183043440681538',
            'ajs_anonymous_id': 'ff7afac45048707f79632325386a217f',
            '_gcl_au': '1.1.51445185.1758638744',
            '_hjSessionUser_640499': 'eyJpZCI6IjRlOTEzM2VmLTcyOTMtNWExZi05OGJlLWQzZjE0MWQ2YjE4MiIsImNyZWF0ZWQiOjE3NTg2Mzg3NDQ0MzYsImV4aXN0aW5nIjp0cnVlX==',
            '_hjHasCachedUserAttributes': 'true',
            '_clck': '1h5hlup%5E2%5Efzl%5E0%5E2092',
            'da_searchTerm': 'undefined',
            '__gads': 'ID=8ad9a68cb5c684fa:T=1758638767:RT=1758722122:S=ALNI_MY4Ytzuptq1nsD4a1_X-t_eJrXyVA',
            '__gpi': 'UID=0000119a3b97aea1:T=1758638767:RT=1758722122:S=ALNI_MZuTETQTZh_ltRrwlkt6v8KFdkSiQ',
            '__eoi': 'ID=e59624fa2967b995:T=1758638767:RT=1758722122:S=AA-Afjahs8Yjg17hOIYmY_KEHh1a',
            'JobseekerSessionId': 'd3183f3b-a12e-4f65-ae9b-06136107c9b6',
            'JobseekerVisitorId': 'd3183f3b-a12e-4f65-ae9b-06136107c9b6',
            'main': 'V%7C2~P%7Cjobsearch~WH%7CJawa%20Barat~WID%7C2030700~OSF%7Cquick&set=1758739139553/V%7C2~P%7Cjobsearch~OSF%7Cquick&set=1758638939137/V%7C2~P%7Cjobsearch~WID%7C2030916~I%7C6281~OSF%7Cquick&set=1758638937615',
            '__cf_bm': '7IwhF1T9.i2d3ucQ4w7Ufi3vDUpxXHRnIBLDQxXCZyA-1758739138-1.0.1.1-H6MCA1NuMCuvJOTB7.fpZWefn.u2kiQEuX18eVj7Of_n6_r_VTLDyhgc3O4VmwBz8auSipt58_KGsyLYQqh8Qn72puFVVPP4K6wwhXIjdFg',
            '_cfuvid': 'pSb5Uac2IzUZLaZ46IyJlowDUtZrTvv7S_0E3iI.BTI-1758739138748-0.0.1.1-604800000',
            'da_sa_candi_sid': '1758739140358',
            'da_cdt': 'visid_019977099112001741f2652009000506f001906700bd0-sesid_1758739140358-hbvid_5b600d91_3699_4b69_8c83_f33134983b1d-tempAcqSessionId_1758739140138-tempAcqVisitorId_5b600d9136994b698c83f33134983b1d',
            '_ga_DSKCDC8253': 'GS2.1.s1758739140$o4$g0$t1758739140$j60$l0$h0',
            'ttcsid': '1758739140408::TDidaf9J31nSWzhsM2QZ.3.1758739140408.0',
            'ttcsid_CR8MQEJC77UC0UOHC250': '1758739139429::_EPMV9w6eKCIOorwHxQo.3.1758739141612.0',
            '_clsk': 'lxc2ni%5E1758739730453%5E2%5E0%5Ey.clarity.ms%2Fcollect',
            'utag_main': 'v_id:019977099112001741f2652009000506f001906700bd0$_sn:3$_se:7%3Bexp-session$_ss:0%3Bexp-session$_st:1758741822946%3Bexp-session$ses_id:1758739140358%3Bexp-session$_pn:1%3Bexp-session$_prevpage:search%20results%3Bexp-1758743622952',
            'hubble_temp_acq_session': 'id%3A1758739140138_end%3A1758741822956_sent%3A19',
            '_dd_s': 'rum=0&expire=1758741359041&logs=0',
            '_uetsid': 'fb5f87f0988b11f09d8ca74108b00878',
            '_uetvid': 'fb5f8c50988b11f0bdd25bb2cc52092b',
        }
        
        self.detail_headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9,id;q=0.8',
            'content-type': 'application/json',
            'origin': 'https://id.jobstreet.com',
            'priority': 'u=1, i',
            'referer': 'https://id.jobstreet.com/id/jobs/in-Jawa-Barat',
            'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'seek-request-brand': 'jobstreet',
            'seek-request-country': 'ID',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
            'x-seek-ec-sessionid': 'b3425f79-1258-4f2d-8f93-c4c825e782c4',
            'x-seek-ec-visitorid': 'b3425f79-1258-4f2d-8f93-c4c825e782c4',
            'x-seek-site': 'chalice',
        }
        
        self.detail_url = 'https://id.jobstreet.com/graphql'
    
    def set_delay(self, delay):
        """Set the delay between requests"""
        self.delay = delay
    
    def get_delay(self):
        """Get the current delay between requests"""
        return self.delay

    def get_single_page_jobs(self, page):
        """Get jobs from a single page"""
        params = self.base_params.copy()
        params['page'] = str(page)
        
        print(f"Scraping JobStreet page {page}...")
        
        try:
            response = requests.get(
                self.base_url,
                params=params,
                cookies=self.cookies,
                headers=self.headers,
            )
            response.raise_for_status()  # Raise an exception for bad status codes
            
            data = response.json()
            jobs = data.get('data', [])

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
        """Get detailed information for a specific job by job ID using GraphQL"""
        import uuid
        
        json_data = {
            'operationName': 'jobDetails',
            'variables': {
                'jobId': str(job_id),
                'jobDetailsViewedCorrelationId': str(uuid.uuid4()),
                'sessionId': 'b3425f79-1258-4f2d-8f93-c4c825e782c4',
                'zone': 'asia-4',
                'locale': 'id-ID',
                'languageCode': 'id',
                'countryCode': 'ID',
                'timezone': 'Asia/Jakarta',
                'visitorId': '5b600d91-3699-4b69-8c83-f33134983b1d',
                'enableApplicantCount': False,
                'enableWorkArrangements': True,
            },
            'query': 'query jobDetails($jobId: ID!, $jobDetailsViewedCorrelationId: String!, $sessionId: String!, $zone: Zone!, $locale: Locale!, $languageCode: LanguageCodeIso!, $countryCode: CountryCodeIso2!, $timezone: Timezone!, $visitorId: UUID!, $enableApplicantCount: Boolean!, $enableWorkArrangements: Boolean!) {\n  jobDetails(\n    id: $jobId\n    tracking: {channel: "WEB", jobDetailsViewedCorrelationId: $jobDetailsViewedCorrelationId, sessionId: $sessionId}\n  ) {\n    ...job\n    insights @include(if: $enableApplicantCount) {\n      ... on ApplicantCount {\n        countLabel(locale: $locale)\n        volumeLabel(locale: $locale)\n        count\n        __typename\n      }\n      __typename\n    }\n    learningInsights(platform: WEB, zone: $zone, locale: $locale) {\n      analytics\n      content\n      __typename\n    }\n    gfjInfo {\n      location {\n        countryCode\n        country(locale: $locale)\n        suburb(locale: $locale)\n        region(locale: $locale)\n        state(locale: $locale)\n        postcode\n        __typename\n      }\n      workTypes {\n        label\n        __typename\n      }\n      company {\n        url(locale: $locale, zone: $zone)\n        __typename\n      }\n      __typename\n    }\n    workArrangements(visitorId: $visitorId, channel: "JDV", platform: WEB) @include(if: $enableWorkArrangements) {\n      arrangements {\n        type\n        label(locale: $locale)\n        __typename\n      }\n      label(locale: $locale)\n      __typename\n    }\n    seoInfo {\n      normalisedRoleTitle\n      workType\n      classification\n      subClassification\n      where(zone: $zone)\n      broaderLocationName(locale: $locale)\n      normalisedOrganisationName\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment job on JobDetails {\n  job {\n    sourceZone\n    tracking {\n      adProductType\n      classificationInfo {\n        classificationId\n        classification\n        subClassificationId\n        subClassification\n        __typename\n      }\n      hasRoleRequirements\n      isPrivateAdvertiser\n      locationInfo {\n        area\n        location\n        locationIds\n        __typename\n      }\n      workTypeIds\n      postedTime\n      __typename\n    }\n    id\n    title\n    phoneNumber\n    isExpired\n    expiresAt {\n      dateTimeUtc\n      __typename\n    }\n    isLinkOut\n    contactMatches {\n      type\n      value\n      __typename\n    }\n    isVerified\n    abstract\n    content(platform: WEB)\n    status\n    listedAt {\n      label(context: JOB_POSTED, length: SHORT, timezone: $timezone, locale: $locale)\n      dateTimeUtc\n      __typename\n    }\n    salary {\n      currencyLabel(zone: $zone)\n      label\n      __typename\n    }\n    shareLink(platform: WEB, zone: $zone, locale: $locale)\n    workTypes {\n      label(locale: $locale)\n      __typename\n    }\n    advertiser {\n      id\n      name(locale: $locale)\n      isVerified\n      registrationDate {\n        dateTimeUtc\n        __typename\n      }\n      __typename\n    }\n    location {\n      label(locale: $locale, type: LONG)\n      __typename\n    }\n    classifications {\n      label(languageCode: $languageCode)\n      __typename\n    }\n    products {\n      branding {\n        id\n        cover {\n          url\n          __typename\n        }\n        thumbnailCover: cover(isThumbnail: true) {\n          url\n          __typename\n        }\n        logo {\n          url\n          __typename\n        }\n        __typename\n      }\n      bullets\n      questionnaire {\n        questions\n        __typename\n      }\n      video {\n        url\n        position\n        __typename\n      }\n      displayTags {\n        label(locale: $locale)\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  companyProfile(zone: $zone) {\n    id\n    name\n    companyNameSlug\n    shouldDisplayReviews\n    branding {\n      logo\n      __typename\n    }\n    overview {\n      description {\n        paragraphs\n        __typename\n      }\n      industry\n      size {\n        description\n        __typename\n      }\n      website {\n        url\n        __typename\n      }\n      __typename\n    }\n    reviewsSummary {\n      overallRating {\n        numberOfReviews {\n          value\n          __typename\n        }\n        value\n        __typename\n      }\n      __typename\n    }\n    perksAndBenefits {\n      title\n      __typename\n    }\n    __typename\n  }\n  companySearchUrl(zone: $zone, languageCode: $languageCode)\n  companyTags {\n    key(languageCode: $languageCode)\n    value\n    __typename\n  }\n  restrictedApplication(countryCode: $countryCode) {\n    label(locale: $locale)\n    __typename\n  }\n  sourcr {\n    image\n    imageMobile\n    link\n    __typename\n  }\n  __typename\n}'
        }
        
        print(f"  Fetching details for job ID: {job_id}")
        
        try:
            response = requests.post(
                self.detail_url,
                cookies=self.detail_cookies,
                headers=self.detail_headers,
                json=json_data
            )
            response.raise_for_status()
            
            data = response.json()
            
            # Extract job detail from GraphQL response
            if 'data' in data and 'jobDetails' in data['data']:
                job_details = data['data']['jobDetails']
                return job_details
            
            return None
            
        except requests.exceptions.RequestException as e:
            print(f"    Error fetching detail for job {job_id}: {e}")
            return None
        except Exception as e:
            print(f"    Unexpected error fetching detail for job {job_id}: {e}")
            return None
    
    def scrape_all_jobs(self, max_pages=None):
        """Scrape all job listings from all pages and save to Excel
        
        Args:
            max_pages (int, optional): Maximum number of pages to scrape. If None, scrape all pages.
        """
        all_jobs = []
        page = 1
        
        if max_pages:
            print(f"Starting JobStreet job scraping (max {max_pages} pages)...")
        else:
            print("Starting JobStreet job scraping (all pages)...")
        
        while True:
            # Check if we've reached the maximum number of pages
            if max_pages and page > max_pages:
                print(f"Reached maximum pages limit ({max_pages}). Stopping...")
                break
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
            pages_scraped = min(page-1, max_pages) if max_pages else page-1
            print(f"Successfully scraped {len(all_jobs)} jobs from {pages_scraped} pages")
        else:
            print("No jobs were scraped")
        
        return all_jobs
    
    def scrape_jobs_list_only(self, max_pages=None):
        """Scrape only job listings without details (faster)
        
        Args:
            max_pages (int, optional): Maximum number of pages to scrape. If None, scrape all pages.
        """
        all_jobs = []
        page = 1
        
        if max_pages:
            print(f"Starting JobStreet job scraping (list only, max {max_pages} pages)...")
        else:
            print("Starting JobStreet job scraping (list only, all pages)...")
        
        while True:
            # Check if we've reached the maximum number of pages
            if max_pages and page > max_pages:
                print(f"Reached maximum pages limit ({max_pages}). Stopping...")
                break
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
            pages_scraped = min(page-1, max_pages) if max_pages else page-1
            print(f"Successfully scraped {len(all_jobs)} jobs from {pages_scraped} pages (list only)")
        else:
            print("No jobs were scraped")
        
        return all_jobs
    
    def flatten_job_data(self, job):
        """Flatten nested job data for Excel compatibility - focused on specific fields"""
        flattened = {}
        
        # Core fields you requested
        flattened['id'] = job.get('id')
        flattened['title'] = job.get('title')
        flattened['teaser'] = job.get('teaser')
        flattened['salary_label'] = job.get('salaryLabel', '')
        
        # Advertiser information
        advertiser = job.get('advertiser', {})
        flattened['advertiser_id'] = advertiser.get('id', '')
        flattened['advertiser_description'] = advertiser.get('description', '')
        
        # Classifications (main classification and subclassification)
        classifications = job.get('classifications', [])
        if classifications and len(classifications) > 0:
            first_classification = classifications[0]
            if 'classification' in first_classification:
                flattened['classification'] = first_classification['classification'].get('description', '')
                flattened['classification_id'] = first_classification['classification'].get('id', '')
            if 'subclassification' in first_classification:
                flattened['subclassification'] = first_classification['subclassification'].get('description', '')
                flattened['subclassification_id'] = first_classification['subclassification'].get('id', '')
        else:
            flattened['classification'] = ''
            flattened['classification_id'] = ''
            flattened['subclassification'] = ''
            flattened['subclassification_id'] = ''
        
        # Locations
        locations = job.get('locations', [])
        if locations and len(locations) > 0:
            location_labels = []
            country_codes = []
            for loc in locations:
                location_labels.append(loc.get('label', ''))
                country_codes.append(loc.get('countryCode', ''))
            flattened['locations'] = '; '.join(location_labels)
            flattened['country_codes'] = '; '.join(country_codes)
        else:
            flattened['locations'] = ''
            flattened['country_codes'] = ''
        
        # Additional useful fields
        flattened['listing_date'] = job.get('listingDate', '')
        flattened['listing_date_display'] = job.get('listingDateDisplay', '')
        flattened['work_types'] = '; '.join(job.get('workTypes', []))
        
        # Work arrangements
        work_arrangements = job.get('workArrangements', {})
        if work_arrangements and 'data' in work_arrangements:
            arrangement_labels = []
            for wa in work_arrangements['data']:
                if isinstance(wa, dict) and 'label' in wa:
                    if isinstance(wa['label'], dict) and 'text' in wa['label']:
                        arrangement_labels.append(wa['label']['text'])
                    else:
                        arrangement_labels.append(str(wa['label']))
            flattened['work_arrangements'] = '; '.join(arrangement_labels)
        else:
            flattened['work_arrangements'] = ''
        
        # Job detail information (if available)
        detail = job.get('detail')
        if detail and 'job' in detail:
            job_detail = detail['job']
            flattened['detail_content'] = job_detail.get('content', '')
            flattened['detail_abstract'] = job_detail.get('abstract', '')
            flattened['detail_phone_number'] = job_detail.get('phoneNumber', '')
            flattened['detail_is_expired'] = job_detail.get('isExpired', '')
            flattened['detail_is_verified'] = job_detail.get('isVerified', '')
            flattened['detail_status'] = job_detail.get('status', '')
            flattened['detail_share_link'] = job_detail.get('shareLink', '')
            
            # Detail listing date
            detail_listed_at = job_detail.get('listedAt', {})
            if detail_listed_at:
                flattened['detail_listed_at_label'] = detail_listed_at.get('label', '')
                flattened['detail_listed_at_utc'] = detail_listed_at.get('dateTimeUtc', '')
            
            # Detail salary
            detail_salary = job_detail.get('salary', {})
            if detail_salary:
                flattened['detail_salary_currency'] = detail_salary.get('currencyLabel', '')
                flattened['detail_salary_label'] = detail_salary.get('label', '')
            
            # Detail advertiser
            detail_advertiser = job_detail.get('advertiser', {})
            if detail_advertiser:
                flattened['detail_advertiser_name'] = detail_advertiser.get('name', '')
                flattened['detail_advertiser_verified'] = detail_advertiser.get('isVerified', '')
            
            # Detail location
            detail_location = job_detail.get('location', {})
            if detail_location:
                flattened['detail_location_label'] = detail_location.get('label', '')
            
            # Detail work types
            detail_work_types = job_detail.get('workTypes')
            if detail_work_types:
                if isinstance(detail_work_types, dict):
                    # Single workTypes object with label field
                    flattened['detail_work_types'] = detail_work_types.get('label', '')
                elif isinstance(detail_work_types, list):
                    # Array of workTypes objects
                    work_type_labels = []
                    for wt in detail_work_types:
                        if isinstance(wt, dict):
                            work_type_labels.append(wt.get('label', ''))
                        elif isinstance(wt, str):
                            work_type_labels.append(wt)
                    flattened['detail_work_types'] = '; '.join(work_type_labels)
            
            # Detail classifications
            detail_classifications = job_detail.get('classifications', [])
            if detail_classifications:
                classification_labels = []
                for c in detail_classifications:
                    if isinstance(c, dict):
                        classification_labels.append(c.get('label', ''))
                    elif isinstance(c, str):
                        classification_labels.append(c)
                flattened['detail_classifications'] = '; '.join(classification_labels)
            
            # Product bullets (key job highlights)
            products = job_detail.get('products')
            if products:
                if isinstance(products, dict):
                    # Single products object with bullets field
                    bullets = products.get('bullets', [])
                    if bullets and isinstance(bullets, list):
                        flattened['detail_bullets'] = '; '.join(bullets)
                elif isinstance(products, list) and len(products) > 0:
                    # Array of products objects
                    first_product = products[0]
                    if isinstance(first_product, dict):
                        bullets = first_product.get('bullets', [])
                        if bullets and isinstance(bullets, list):
                            flattened['detail_bullets'] = '; '.join(bullets)
        
        # Detail work arrangements (from job detail API)
        if detail and 'workArrangements' in detail:
            work_arrangements_detail = detail['workArrangements']
            if work_arrangements_detail and 'arrangements' in work_arrangements_detail:
                arrangement_labels = []
                for arr in work_arrangements_detail['arrangements']:
                    if isinstance(arr, dict):
                        arrangement_labels.append(arr.get('label', ''))
                if arrangement_labels:
                    flattened['detail_work_arrangements'] = '; '.join(arrangement_labels)
        
        # Company profile information (if available)
        if detail and 'companyProfile' in detail:
            company_profile = detail['companyProfile']
            if company_profile:
                flattened['company_name'] = company_profile.get('name', '')
                
                # Company overview
                overview = company_profile.get('overview', {})
                if overview:
                    description = overview.get('description', {})
                    if description and 'paragraphs' in description:
                        flattened['company_description'] = '; '.join(description['paragraphs'])
                    
                    flattened['company_industry'] = overview.get('industry', '')
                    
                    size = overview.get('size', {})
                    if size:
                        flattened['company_size'] = size.get('description', '')
                    
                    website = overview.get('website', {})
                    if website:
                        flattened['company_website'] = website.get('url', '')
                
                # Company reviews
                reviews_summary = company_profile.get('reviewsSummary', {})
                if reviews_summary and 'overallRating' in reviews_summary:
                    overall_rating = reviews_summary['overallRating']
                    flattened['company_rating'] = overall_rating.get('value', '')
                    
                    num_reviews = overall_rating.get('numberOfReviews', {})
                    if num_reviews:
                        flattened['company_review_count'] = num_reviews.get('value', '')
        
        return flattened
    
    def save_to_excel(self, jobs_data):
        """Save jobs data to Excel file"""
        df = pd.DataFrame(jobs_data)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"jobstreet_jobs_{timestamp}.xlsx"
        
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
            csv_filename = f"jobstreet_jobs_{timestamp}.csv"
            df.to_csv(csv_filename, index=False)
            print(f"Fallback: Data saved to {csv_filename}")


# Run the scraper
if __name__ == "__main__":
    scraper = JobStreetScraper()
    
    # Choose scraping method:
    # Option 1: Scrape with job details (slower but more comprehensive)
    print("Starting comprehensive JobStreet scraping with job details...")
    # scraper.scrape_all_jobs()  # Scrape all pages
    
    # Option 2: Scrape only first 3 pages with details
    scraper.scrape_all_jobs(max_pages=3)
    
    # Option 3: Scrape only first 5 pages without details (faster)
    # scraper.scrape_jobs_list_only(max_pages=5)
    
    # Option 4: Scrape all pages without details (faster)
    # scraper.scrape_jobs_list_only()


