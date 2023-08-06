import requests
import json
from collections import defaultdict

base_url = "https://members-api.parliament.uk/api/Members"

data = defaultdict(list)

# 1 = House of Commons, 2 = House of Lords
response = requests.get(f"{base_url}/Search", params={"House": 1})

# Check if the request was successful
if response.status_code == 200:    
    total_results = response.json()['totalResults']        
    results_per_page = 20    
    num_pages = total_results // results_per_page + (total_results % results_per_page > 0)

    
    def process_page(items):
        for item in items:
            if item['value']['latestHouseMembership']['membershipEndDate'] is None: # Is current MP
                # Fetch contact details
                print(f"Fetching contact details for {item['value']['nameDisplayAs']} ...", flush=True)
                contact_response = requests.get(f"{base_url}/{item['value']['id']}/Contact")
                if contact_response.status_code == 200:
                    contact_info = contact_response.json()['value']                    
                    for contact in contact_info:
                        contact['id'] = item['value']['id']
                        contact['name'] = item['value']['nameDisplayAs']
                        contact['constituency'] = item['value']['latestHouseMembership']['membershipFrom']
                        
                        info = {
                            "type": contact["type"],
                            "typeDescription": contact["typeDescription"],
                            "typeId": contact["typeId"],
                            "isPreferred": contact["isPreferred"],
                            "isWebAddress": contact["isWebAddress"],
                            "notes": contact["notes"],
                            "line1": contact["line1"],
                            "line5": contact.get("line5", None),  # Some entries might not have all fields
                            "postcode": contact.get("postcode", None),
                            "phone": contact.get("phone", None),
                            "email": contact.get("email", None),
                            "line2": contact.get("line2", None)
                        }
                        # Remove None values
                        info = {k: v for k, v in info.items() if v is not None}
                        
                        data[(contact['id'], contact['name'], contact['constituency'])].append(info)

    # Process the first page
    process_page(response.json()['items'])

    # Get the rest of the pages
    for page in range(2, num_pages + 1):        
        response = requests.get(f"{base_url}/Search", params={"House": 1, "skip": (page - 1) * results_per_page, "take": results_per_page})
        
        if response.status_code == 200:
            process_page(response.json()['items'])
        else:
            print(f"Request for page {page} failed with status code {response.status_code}")
            break
else:
    print(f"Initial request failed with status code {response.status_code}")

# Reformat data
final_data = []
for (id_, name, constituency), info in data.items():
    final_data.append({
        "id": id_,
        "name": name,
        "constituency": constituency,
        "data": info
    })

with open('HoC_current.json', 'w') as f:
    json.dump(final_data, f, indent=4)
