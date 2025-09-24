import requests

cookies = {
    'device_id': 'b5c89ca4-21a1-45c7-b276-3b786e897010',
    '_gcl_au': '1.1.892705639.1758724866',
    'sessionFirstTouchPath': '/id',
    '_ga': 'GA1.1.1633647662.1758724867',
    'airbridge_migration_metadata__taplokerbyglints': '%7B%22version%22%3A%221.10.78%22%7D',
    'ab180ClientId': 'c3c9ab1e-77b7-41a1-a02b-0db945db2dba',
    '_fbp': 'fb.1.1758724867476.59351549549642190',
    '_tt_enable_cookie': '1',
    '_ttp': '01K5Y2QHK3PRN35DHHJTBYE973_.tt.1',
    'g_state': '{"i_l":0}',
    'session': 'Fe26.2**5bb2746ec36795769a682d1947387bcbf9fdf3986a4566577df37662a3af50c7*mLhCFTczfAocat85kQ-v-g*51D-zOpM8-2to6pC8mgSRqPtV8scF430Deprx3ElKuSXLc8xk_ICMvxc6_QbpuPF**b89cb2843ae3cc0225b8d9312ff6835e705443c99027738b67adc51b3ec7f680*wa-n7tmaL6cfkW9ahBPfwvQXV71AIh6JqZnLZ3SEInY',
    'airbridge_user': '%7B%22attributes%22%3A%7B%22country_code%22%3A%22ID%22%2C%22user_email%22%3A%22dopokan1@gmail.com%22%2C%22role%22%3A%22CANDIDATE%22%2C%22days_from_signup%22%3A0%2C%22has_whatsapp_number%22%3Afalse%2C%22has_resume%22%3Afalse%2C%22has_mobile_number%22%3Afalse%2C%22age_in_years%22%3A%22null%22%2C%22gender%22%3A%22%22%2C%22number_of_skills_listed%22%3A0%2C%22utm_referrer%22%3A%22explore%22%7D%2C%22externalUserID%22%3A%22863a8cdd-5b0f-449a-b94a-b0d9d3d6638e%22%2C%22externalUserEmail%22%3A%22dopokan1@gmail.com%22%7D',
    'pastJobSearchConditions': '%5B%5D',
    'currentJobID': 'cd7a2951-e7cc-4bd0-af14-676cf2377208',
    'traceInfo': '%7B%22expInfo%22%3A%22mgtExperimentWebFYPMultRetrievals%3Abase%2CmgtDstExperimentRecmdApplication%3Abase_0210_decay_3%2CmgtDstExperimentRecmdPaidJob%3Aexp_2_1206%2CmgtDstExperimentRecmdConversionRate%3Agroup_10_0812%2CmgtDstExpSalaryWeight%3Aexp_0619_w3%2CmgtDstExpUserTrafficControlByScore%3Aexperiment%2CmgtDstExpFYPJobType%3Abase_0828%2CmgtDstExpFYPAge%3Aexp_0830_w2%2CmgtMobExperimentJobCardUI%3Aexp_new_1227%2CmgtOneTapApplyVIPJobs%3AB%22%2C%22requestId%22%3A%221dc01be4b2473f1f04207bce54e0b46e%22%7D',
    'airbridge_touchpoint': '%7B%22channel%22%3A%22glints.com%22%2C%22parameter%22%3A%7B%7D%2C%22generationType%22%3A1224%2C%22url%22%3A%22https%3A//glints.com/id/opportunities/jobs/teknisi-service-laptop-dan-pc/cd7a2951-e7cc-4bd0-af14-676cf2377208%3Futm_referrer%3Dexplore%26traceInfo%3D55b3fd8dfe59b4c421e4d43407b3d80d%22%2C%22timestamp%22%3A1758745791012%7D',
    'airbridge_session': '%7B%22id%22%3A%225c36b656-c505-4103-a3f9-44d7155a8a9e%22%2C%22timeout%22%3A1800000%2C%22start%22%3A1758745611292%2C%22end%22%3A1758745791171%7D',
    'glints_tracking_id': '10b0f385-9011-466e-a1fc-0570c9797cb6',
    'sessionLastTouchPath': '/id/opportunities/jobs/explore',
    'sessionIsLastTouch': 'true',
    'ttcsid': '1758749428718::3nqM6vYZH0dSKQlFNX8Q.4.1758749439114.0',
    '_ga_FQ75P4PXDH': 'GS2.1.s1758749401$o5$g1$t1758749440$j21$l0$h0',
    'ttcsid_CDIDC9JC77U9O4C7VUEG': '1758749426766::aGKrl9dkq2RlZrUSaCVc.4.1758749650024.0',
}

headers = {
    'accept': '*/*',
    'accept-language': 'id',
    'content-type': 'application/json',
    'origin': 'https://glints.com',
    'priority': 'u=1, i',
    'referer': 'https://glints.com/id/opportunities/jobs/explore?country=ID&locationId=06c9e480-42e7-4f11-9d6c-67ad64ccc0f6&locationName=Jawa+Barat&lowestLocationLevel=2&educationLevel=HIGH_SCHOOL',
    'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'traceparent': '00-2266e05aeba59172d00e496ffab7b733-c334318263814fcf-01',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
    'x-glints-country-code': 'ID',
    # 'cookie': 'device_id=b5c89ca4-21a1-45c7-b276-3b786e897010; _gcl_au=1.1.892705639.1758724866; sessionFirstTouchPath=/id; _ga=GA1.1.1633647662.1758724867; airbridge_migration_metadata__taplokerbyglints=%7B%22version%22%3A%221.10.78%22%7D; ab180ClientId=c3c9ab1e-77b7-41a1-a02b-0db945db2dba; _fbp=fb.1.1758724867476.59351549549642190; _tt_enable_cookie=1; _ttp=01K5Y2QHK3PRN35DHHJTBYE973_.tt.1; g_state={"i_l":0}; session=Fe26.2**5bb2746ec36795769a682d1947387bcbf9fdf3986a4566577df37662a3af50c7*mLhCFTczfAocat85kQ-v-g*51D-zOpM8-2to6pC8mgSRqPtV8scF430Deprx3ElKuSXLc8xk_ICMvxc6_QbpuPF**b89cb2843ae3cc0225b8d9312ff6835e705443c99027738b67adc51b3ec7f680*wa-n7tmaL6cfkW9ahBPfwvQXV71AIh6JqZnLZ3SEInY; airbridge_user=%7B%22attributes%22%3A%7B%22country_code%22%3A%22ID%22%2C%22user_email%22%3A%22dopokan1@gmail.com%22%2C%22role%22%3A%22CANDIDATE%22%2C%22days_from_signup%22%3A0%2C%22has_whatsapp_number%22%3Afalse%2C%22has_resume%22%3Afalse%2C%22has_mobile_number%22%3Afalse%2C%22age_in_years%22%3A%22null%22%2C%22gender%22%3A%22%22%2C%22number_of_skills_listed%22%3A0%2C%22utm_referrer%22%3A%22explore%22%7D%2C%22externalUserID%22%3A%22863a8cdd-5b0f-449a-b94a-b0d9d3d6638e%22%2C%22externalUserEmail%22%3A%22dopokan1@gmail.com%22%7D; pastJobSearchConditions=%5B%5D; currentJobID=cd7a2951-e7cc-4bd0-af14-676cf2377208; traceInfo=%7B%22expInfo%22%3A%22mgtExperimentWebFYPMultRetrievals%3Abase%2CmgtDstExperimentRecmdApplication%3Abase_0210_decay_3%2CmgtDstExperimentRecmdPaidJob%3Aexp_2_1206%2CmgtDstExperimentRecmdConversionRate%3Agroup_10_0812%2CmgtDstExpSalaryWeight%3Aexp_0619_w3%2CmgtDstExpUserTrafficControlByScore%3Aexperiment%2CmgtDstExpFYPJobType%3Abase_0828%2CmgtDstExpFYPAge%3Aexp_0830_w2%2CmgtMobExperimentJobCardUI%3Aexp_new_1227%2CmgtOneTapApplyVIPJobs%3AB%22%2C%22requestId%22%3A%221dc01be4b2473f1f04207bce54e0b46e%22%7D; airbridge_touchpoint=%7B%22channel%22%3A%22glints.com%22%2C%22parameter%22%3A%7B%7D%2C%22generationType%22%3A1224%2C%22url%22%3A%22https%3A//glints.com/id/opportunities/jobs/teknisi-service-laptop-dan-pc/cd7a2951-e7cc-4bd0-af14-676cf2377208%3Futm_referrer%3Dexplore%26traceInfo%3D55b3fd8dfe59b4c421e4d43407b3d80d%22%2C%22timestamp%22%3A1758745791012%7D; airbridge_session=%7B%22id%22%3A%225c36b656-c505-4103-a3f9-44d7155a8a9e%22%2C%22timeout%22%3A1800000%2C%22start%22%3A1758745611292%2C%22end%22%3A1758745791171%7D; glints_tracking_id=10b0f385-9011-466e-a1fc-0570c9797cb6; sessionLastTouchPath=/id/opportunities/jobs/explore; sessionIsLastTouch=true; ttcsid=1758749428718::3nqM6vYZH0dSKQlFNX8Q.4.1758749439114.0; _ga_FQ75P4PXDH=GS2.1.s1758749401$o5$g1$t1758749440$j21$l0$h0; ttcsid_CDIDC9JC77U9O4C7VUEG=1758749426766::aGKrl9dkq2RlZrUSaCVc.4.1758749650024.0',
}

params = {
    'op': 'searchJobsV3',
}

json_data = {
    'operationName': 'searchJobsV3',
    'variables': {
        'data': {
            'CountryCode': 'ID',
            'LocationIds': [
                '06c9e480-42e7-4f11-9d6c-67ad64ccc0f6',
            ],
            'educationLevels': [
                'HIGH_SCHOOL',
            ],
            'includeExternalJobs': True,
            'pageSize': 30,
            'page': 2,
        },
    },
    'query': 'query searchJobsV3($data: JobSearchConditionInput!) {\n  searchJobsV3(data: $data) {\n    jobsInPage {\n      id\n      title\n      workArrangementOption\n      status\n      createdAt\n      updatedAt\n      isActivelyHiring\n      isHot\n      isApplied\n      shouldShowSalary\n      educationLevel\n      type\n      fraudReportFlag\n      salaryEstimate {\n        minAmount\n        maxAmount\n        CurrencyCode\n        __typename\n      }\n      company {\n        ...CompanyFields\n        __typename\n      }\n      citySubDivision {\n        id\n        name\n        __typename\n      }\n      city {\n        ...CityFields\n        __typename\n      }\n      country {\n        ...CountryFields\n        __typename\n      }\n      salaries {\n        ...SalaryFields\n        __typename\n      }\n      location {\n        ...LocationFields\n        __typename\n      }\n      minYearsOfExperience\n      maxYearsOfExperience\n      source\n      type\n      hierarchicalJobCategory {\n        id\n        level\n        name\n        children {\n          name\n          level\n          id\n          __typename\n        }\n        parents {\n          id\n          level\n          name\n          __typename\n        }\n        __typename\n      }\n      skills {\n        skill {\n          id\n          name\n          __typename\n        }\n        mustHave\n        __typename\n      }\n      traceInfo\n      __typename\n    }\n    expInfo\n    hasMore\n    __typename\n  }\n}\n\nfragment CompanyFields on Company {\n  id\n  name\n  logo\n  status\n  isVIP\n  IndustryId\n  industry {\n    id\n    name\n    __typename\n  }\n  verificationTier {\n    type\n    __typename\n  }\n  __typename\n}\n\nfragment CityFields on City {\n  id\n  name\n  __typename\n}\n\nfragment CountryFields on Country {\n  code\n  name\n  __typename\n}\n\nfragment SalaryFields on JobSalary {\n  id\n  salaryType\n  salaryMode\n  maxAmount\n  minAmount\n  CurrencyCode\n  __typename\n}\n\nfragment LocationFields on HierarchicalLocation {\n  id\n  name\n  administrativeLevelName\n  formattedName\n  level\n  slug\n  latitude\n  longitude\n  parents {\n    id\n    name\n    administrativeLevelName\n    formattedName\n    level\n    slug\n    CountryCode: countryCode\n    parents {\n      level\n      formattedName\n      slug\n      __typename\n    }\n    __typename\n  }\n  __typename\n}',
}

response = requests.post('https://glints.com/api/v2-alc/graphql', params=params, cookies=cookies, headers=headers, json=json_data)

# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
#data = '{"operationName":"searchJobsV3","variables":{"data":{"CountryCode":"ID","LocationIds":["06c9e480-42e7-4f11-9d6c-67ad64ccc0f6"],"educationLevels":["HIGH_SCHOOL"],"includeExternalJobs":true,"pageSize":30,"page":2}},"query":"query searchJobsV3($data: JobSearchConditionInput!) {\\n  searchJobsV3(data: $data) {\\n    jobsInPage {\\n      id\\n      title\\n      workArrangementOption\\n      status\\n      createdAt\\n      updatedAt\\n      isActivelyHiring\\n      isHot\\n      isApplied\\n      shouldShowSalary\\n      educationLevel\\n      type\\n      fraudReportFlag\\n      salaryEstimate {\\n        minAmount\\n        maxAmount\\n        CurrencyCode\\n        __typename\\n      }\\n      company {\\n        ...CompanyFields\\n        __typename\\n      }\\n      citySubDivision {\\n        id\\n        name\\n        __typename\\n      }\\n      city {\\n        ...CityFields\\n        __typename\\n      }\\n      country {\\n        ...CountryFields\\n        __typename\\n      }\\n      salaries {\\n        ...SalaryFields\\n        __typename\\n      }\\n      location {\\n        ...LocationFields\\n        __typename\\n      }\\n      minYearsOfExperience\\n      maxYearsOfExperience\\n      source\\n      type\\n      hierarchicalJobCategory {\\n        id\\n        level\\n        name\\n        children {\\n          name\\n          level\\n          id\\n          __typename\\n        }\\n        parents {\\n          id\\n          level\\n          name\\n          __typename\\n        }\\n        __typename\\n      }\\n      skills {\\n        skill {\\n          id\\n          name\\n          __typename\\n        }\\n        mustHave\\n        __typename\\n      }\\n      traceInfo\\n      __typename\\n    }\\n    expInfo\\n    hasMore\\n    __typename\\n  }\\n}\\n\\nfragment CompanyFields on Company {\\n  id\\n  name\\n  logo\\n  status\\n  isVIP\\n  IndustryId\\n  industry {\\n    id\\n    name\\n    __typename\\n  }\\n  verificationTier {\\n    type\\n    __typename\\n  }\\n  __typename\\n}\\n\\nfragment CityFields on City {\\n  id\\n  name\\n  __typename\\n}\\n\\nfragment CountryFields on Country {\\n  code\\n  name\\n  __typename\\n}\\n\\nfragment SalaryFields on JobSalary {\\n  id\\n  salaryType\\n  salaryMode\\n  maxAmount\\n  minAmount\\n  CurrencyCode\\n  __typename\\n}\\n\\nfragment LocationFields on HierarchicalLocation {\\n  id\\n  name\\n  administrativeLevelName\\n  formattedName\\n  level\\n  slug\\n  latitude\\n  longitude\\n  parents {\\n    id\\n    name\\n    administrativeLevelName\\n    formattedName\\n    level\\n    slug\\n    CountryCode: countryCode\\n    parents {\\n      level\\n      formattedName\\n      slug\\n      __typename\\n    }\\n    __typename\\n  }\\n  __typename\\n}"}'
#response = requests.post('https://glints.com/api/v2-alc/graphql', params=params, cookies=cookies, headers=headers, data=data)
print(response.text)