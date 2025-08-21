# ==============================================================================
# MAIN EXECUTION SCRIPT
# Purpose: Run the main logic of the property ownership scraper.
# ==============================================================================
import time
import os
from scraper import fetch_property_data, parse_owner_info
from file_io import load_data, save_data
import config

def compare_data(old_data: dict, new_data: dict):
    """
    Compares two dictionaries of property data (keyed by parcel number) and identifies differences.
    Each value in the dictionary is expected to be another dictionary containing 'owner_name' and 'address'.
    """
    changes = []
    old_parcels = set(old_data.keys())
    new_parcels = set(new_data.keys())

    # Check for changes on existing properties
    for parcel in old_parcels.intersection(new_parcels):
        old_info = old_data[parcel]
        new_info = new_data[parcel]

        # Compare owner name
        if old_info.get('owner_name') != new_info.get('owner_name'):
            changes.append(
                f"OWNER CHANGE DETECTED for Parcel {parcel}:\n"
                f"  - OLD Owner: {old_info.get('owner_name', 'N/A')}\n"
                f"  - NEW Owner: {new_info.get('owner_name', 'N/A')}"
            )
        # Compare address (if you want to track address changes too)
        if old_info.get('address') != new_info.get('address'):
            changes.append(
                f"ADDRESS CHANGE DETECTED for Parcel {parcel}:\n"
                f"  - OLD Address: {old_info.get('address', 'N/A')}\n"
                f"  - NEW Address: {new_info.get('address', 'N/A')}"
            )

    # Check for new properties
    for parcel in new_parcels - old_parcels:
        new_info = new_data[parcel]
        changes.append(
            f"NEW PROPERTY FOUND: Parcel {parcel}, "
            f"Owner: {new_info.get('owner_name', 'N/A')}, "
            f"Address: {new_info.get('address', 'N/A')}"
        )

    # Check for removed properties
    for parcel in old_parcels - new_parcels:
        old_info = old_data[parcel]
        changes.append(
            f"REMOVED PROPERTY: Parcel {parcel}, "
            f"Last Known Owner: {old_info.get('owner_name', 'N/A')}, "
            f"Last Known Address: {old_info.get('address', 'N/A')}"
        )

    return changes

def main():
    """Main function to run the property scraper and comparison."""
    print("\n--- Anderson County Property Ownership Monitor ---")

    current_properties = {}
    for street in config.STREETS_TO_CHECK:
        html = fetch_property_data(config.BASE_URL, street)
        if html:
            # parse_owner_info now returns a list of dictionaries
            street_properties_list = parse_owner_info(html)
            
            if not street_properties_list:
                print(f"Warning: No properties found for '{street}'. It may be an invalid street name or have no results.")
            
            # Convert the list of dictionaries into a single dictionary keyed by parcel_number
            # This aligns with how `current_properties` is expected to be structured for comparison.
            for prop in street_properties_list:
                parcel = prop.get('parcel_number')
                if parcel and parcel != "N/A": # Ensure parcel number is valid
                    current_properties[parcel] = {
                        "owner_name": prop.get('owner_name', 'N/A'),
                        "address": prop.get('address', 'N/A')
                    }
        # Be respectful to the server and add a small delay
        time.sleep(1)

    if not current_properties:
        print("\nCould not retrieve any property data. Exiting.")
        return

    print(f"\nFinished fetching. Found data for {len(current_properties)} properties.")

    # Check if a local data file exists
    if not os.path.exists(config.DATA_FILE_PATH):
        print("\nFirst run detected. No local data file found.")
        save_data(current_properties, config.DATA_FILE_PATH)
    else:
        print(f"\nFound existing data file. Comparing for changes...")
        previous_properties = load_data(config.DATA_FILE_PATH)
        
        # Ensure previous_properties is also structured correctly for comparison
        # (i.e., keyed by parcel number with nested dicts for owner/address)
        # If load_data might return an old format, you might need a conversion step here
        # For now, assuming load_data will return data compatible with the new structure
        
        changes_found = compare_data(previous_properties, current_properties)

        if not changes_found:
            print("\n--- RESULT: No changes detected. Your data file is up to date. ---")
        else:
            print("\n" + "="*25)
            print("!!! CHANGES DETECTED !!!")
            print("="*25 + "\n")
            for change in changes_found:
                print(f"- {change}\n")

            try:
                confirm = input("Do you want to overwrite the data file with this new data? (y/n): ").lower()
                if confirm == 'y':
                    save_data(current_properties, config.DATA_FILE_PATH)
                else:
                    print("\nUpdate cancelled. The data file was not changed.")
            except KeyboardInterrupt:
                 print("\nUpdate cancelled by user. The data file was not changed.")

if __name__ == "__main__":
    main()
