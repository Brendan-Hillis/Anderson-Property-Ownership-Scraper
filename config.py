# ==============================================================================
# CONFIGURATION
# Purpose: Set up all the variables you might want to change.
# ==============================================================================

# A list of street names you want to check.
# The script will automatically format them for the URL.
STREETS_TO_CHECK = [
    "Parkside Dr",
    "Garden Park dr",
    "turnberry Rd",
    "Tully Dr",
    "Winmar Dr",
    "Stone Cottage Dr",
    "Courtyard Dr",
    "Grove Park Dr"
    # Add more street names here
]

# The base URL for the search query.
BASE_URL = "https://acpass.andersoncountysc.org/asrmain.cgi"

# The name of the file to store the property data.
DATA_FILE_PATH = "property_owners.json"
