import requests

# Function to fetch service entities and frameworks from Port's API
def fetch_service_entities(api_url, headers):
    try:
        URL = f"{api_url}/v1/blueprints/service/entities?exclude_calculated_properties=false&attach_title_to_relation=false"
        response = requests.get(URL, headers=headers)
        response.raise_for_status()  # Raise exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching service entities: {e}")
        return None

# Function to calculate EOL packages for a service entity
def calculate_eol_packages(api_url,headers,service_entity,relate_entity_identifier,blueprint):
    frameworks = service_entity.get("relations", {}).get(relate_entity_identifier,[])
    eol_packages_count = 0
    # Counting packages marked as EOL
    for framework in frameworks:
        state = check_framwork_state(api_url, headers,blueprint, framework)
        if state == "EOL":
            eol_packages_count += 1
    return eol_packages_count

def check_framwork_state(api_url,headers,blueprint_identifier,framework):
    try:
        URL = f"{api_url}/v1/blueprints/{blueprint_identifier}/entities?exclude_calculated_properties=false&attach_title_to_relation=false"
        response = requests.get(URL,headers=headers)
        response.raise_for_status()
        for entity in response.json().get('entities',[]):
            if entity['identifier'] == framework:
                return entity['properties'].get('state')
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
    api_url = input("Please enter api base URL : ")  # Example API endpoint
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
    relate_entity_identifier = input("Please enter the relate entity identifier : ")
    blueprint = input("Please enter the blueprint with the saved pakages :")
    for entity in entities:
        # Step 3: Calculate EOL packages
        eol_packages_count = calculate_eol_packages(api_url, headers,entity,relate_entity_identifier,blueprint)
        print(eol_packages_count)
        # Step 4: Update EOL package count for the service entity
        update_eol_package_count(entity.get("identifier"), eol_packages_count, api_url, headers)
    
        
        
        

# Entry point of the script
if __name__ == "__main__":
    main()

#"https://api.getport.io/"