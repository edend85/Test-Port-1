import requests

# function to fetch service entities and frameworks from Port's API
def fetch_service_entities(api_url, headers):
    try:
        URL = f"{api_url}/v1/blueprints/service/entities?exclude_calculated_properties=false&attach_title_to_relation=false"
        response = requests.get(URL, headers=headers)
        response.raise_for_status()  # Raise exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching service entities: {e}")
        return None

# function to calculate EOL packages for a service entity
def calculate_eol_packages(service_entity,relate_entity_identifier,all_EOL_frameworks):
    framework_for_entity = service_entity.get("relations", {}).get(relate_entity_identifier,[]) #all the framework from specific entity
    eol_packages_count = 0 # reseting the number of pakages so the previous number won't calcluate

    # counting packages marked as EOL
    for FOE in framework_for_entity:
        for EOLframework in all_EOL_frameworks:
            if FOE == EOLframework['identifier']:
                eol_packages_count += 1     
    return eol_packages_count

def fetch_all_EOL_frameworks(api_url,headers,blueprint_identifier):
    all_EOL_frameworks = []
    try:
        URL = f"{api_url}/v1/blueprints/{blueprint_identifier}/entities?exclude_calculated_properties=false&attach_title_to_relation=false"
        response = requests.get(URL,headers=headers)
        response.raise_for_status()
        all_frameworks = response.json().get('entities',[])
        for framework in all_frameworks:
            if framework['properties']['state'] == "EOL":
                all_EOL_frameworks.append(framework)
        return all_EOL_frameworks
    except requests.RequestException as e:
        print(f"An error occurred: {e}")

# Function to update EOL package count for a service entity
def update_eol_package_count(service_entity_identifier, eol_count, api_url, headers):
    update_payload = {
        "properties": {
            "number_of_eol_packages": eol_count
        }
    }
    try:
        url = f"{api_url}/v1/blueprints/service/entities/{service_entity_identifier}?create_missing_related_entities=false"
        response = requests.patch(url, headers=headers, json=update_payload)
        response.raise_for_status()  # Raise exception for HTTP errors
        print(f"EOL package count updated successfully for entity {service_entity_identifier}")
    except requests.exceptions.RequestException as e:
        print(f"Error updating EOL package count: {e}")

# Main function to orchestrate the process
def main():
    api_url = "https://api.getport.io"  # Example API endpoint
    headers = {
        "Authorization":input("Please enter your API key : "),
        "Content-Type": "application/json"
    }

    # Step 1: Fetch service entities from Port's API
    entities_response = fetch_service_entities(api_url, headers)
    if entities_response is None:
        return
    
    entities = entities_response.get("entities", [])
       
    # Step 2: Process each service entity
    all_EOL_frameworks = fetch_all_EOL_frameworks(api_url, headers,"framework") # all EOL framworks from framework blueprint
    for entity in entities:
        # Step 3: Calculate EOL packages
        eol_packages_count = calculate_eol_packages(entity,"framework",all_EOL_frameworks)
        # Step 4: Update EOL package count for the service entity
        update_eol_package_count(entity.get("identifier"), eol_packages_count, api_url, headers)
    
        
        
        

# Entry point of the script
if __name__ == "__main__":
    main()

#"https://api.getport.io/"