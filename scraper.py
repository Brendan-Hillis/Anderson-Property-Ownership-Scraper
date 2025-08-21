# ==============================================================================
# SCRAPER FUNCTIONS
# Purpose: Functions for fetching and parsing data from the website.
# ==============================================================================
import requests
from bs4 import BeautifulSoup

def fetch_property_data(base_url: str, street_name: str):
    """
    Fetches the HTML content for a given street name from the county website.
    """
    params = {
        'QryName': '', 'QryMapNo': '', 'QryStreet': street_name,
        'Sumbit.x': '41', 'Sumbit.y': '18'
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        print(f"Fetching data for '{street_name}'...")
        response = requests.get(base_url, params=params, headers=headers, timeout=20)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {street_name}: {e}")
        return None

def parse_owner_info(html_content: str):
    """
    Parses the HTML to extract property parcel numbers, owner names, and addresses
    by navigating the document structure directly.
    """
    if not html_content:
        return [] # Return an empty list if no content

    soup = BeautifulSoup(html_content, 'lxml')
    properties_list = []

    # Strategy: Find the main table that contains the data.
    # Based on the sample HTML, the data table is inside a form, which is
    # inside another table. It also has specific border/padding attributes.
    # We'll look for the table that has border=1, cellpadding=0, cellspacing=0,
    # and bordercolor="#003300". This makes the selection more robust than nth-child.
    
    # First, find the form element, as the target table is nested within it.
    # The form has specific attributes like METHOD="POST" and ACTION="asrdetail1.cgi"
    target_form = soup.find('form', attrs={'method': 'POST', 'action': 'asrdetail1.cgi'})

    if target_form:
        # Now, find the table within this form that holds the property data.
        # This table has a border and specific bordercolor.
        target_table = target_form.find('table', attrs={
            'border': '1',
            'cellpadding': '0',
            'cellspacing': '0',
            'bordercolor': '#003300'
        })

        if target_table:
            # Assuming the property rows are direct children <tr> tags of the table's <tbody>.
            # We skip the first row [1:] if it's a header row.
            result_rows = target_table.find_all('tr')[1:]

            for row in result_rows:
                columns = row.find_all('td')
                # Ensure there are enough columns to extract data (at least 5 for owner and address)
                if len(columns) >= 5:
                    try:
                        # Owner's name is in the second <td> (index 1), typically inside an <a> tag
                        owner_tag = columns[1].find('a')
                        owner_name = owner_tag.text.strip() if owner_tag else "N/A"

                        # Address is in the fifth <td> (index 4)
                        address = columns[4].get_text(strip=True)

                        # Parcel number from the input checkbox in the first <td> (index 0)
                        parcel_input = columns[0].find('input', {'name': 'mapno'})
                        parcel_number = parcel_input.get('value') if parcel_input else "N/A"

                        properties_list.append({
                            "parcel_number": parcel_number,
                            "owner_name": owner_name,
                            "address": address
                        })
                    except (AttributeError, IndexError) as e:
                        print(f"Could not parse a row. Skipping. Error: {e}")
                        continue
        else:
            print(f"Warning: Target property table not found within the form.")
    else:
        print(f"Warning: Target form not found. Unable to locate the property data table.")

    return properties_list # Return the list of extracted properties
