# Anderson-Property-Ownership-Scraper

This Python script is designed to monitor property ownership and address changes for specified streets in Anderson County, SC, by scraping data from the official county public access website. It fetches current property information, compares it against a previously saved dataset, and reports any detected changes (new properties, removed properties, or changes in owner/address).
gi
## **🌟 Features**

* **Automated Data Fetching**: Retrieves property data for a list of predefined streets.  
* **Robust Parsing**: Utilizes BeautifulSoup to navigate complex HTML structures and extract relevant owner names, addresses, and parcel numbers.  
* **Change Detection**: Compares the newly scraped data with a local JSON file to identify differences.  
* **Detailed Reporting**: Provides clear messages on new properties, removed properties, and changes in ownership or address for existing parcels.  
* **Persistent Storage**: Saves the latest property data to a JSON file, allowing for historical tracking.

## **📂 File Structure**

The project consists of the following files:

.  
├── main.py  
├── scraper.py  
├── file\_io.py  
├── config.py  
└── requirements.txt

* **main.py**: The main execution script. It orchestrates the data fetching, parsing, comparison, and saving processes. This is the file you'll run.  
* **scraper.py**: Contains functions responsible for web scraping, including fetch\_property\_data (to get HTML content) and parse\_owner\_info (to extract structured data from HTML).  
* **file\_io.py**: Provides utility functions for loading data from and saving data to a JSON file.  
* **config.py**: Stores configurable variables such as the list of street names to check, the base URL for the scraper, and the data file path.  
* **requirements.txt**: Lists all the necessary Python packages required to run the project.

## **🚀 Getting Started**

Follow these steps to set up and run the scraper on your local machine.

### **Prerequisites**

* Python 3.x installed on your system.

### **Installation**

1. **Clone the repository** (or download the files directly) to your local machine:  
   git clone \<your-repository-url\>  
   cd \<your-repository-name\>

2. **Create a virtual environment** (recommended):  
   python \-m venv venv

3. **Activate the virtual environment**:  
   * **Windows (Command Prompt/PowerShell):**  
     .\\venv\\Scripts\\activate

   * **macOS/Linux (Bash/Zsh):**  
     source venv/bin/activate

4. **Install the required packages**:  
   pip install \-r requirements.txt

## **🛠️ Configuration**

Before running the script, you should customize the config.py file:

* **STREETS\_TO\_CHECK**: Add or remove street names that you want to monitor. Ensure they are correctly formatted as strings in the list.  
  STREETS\_TO\_CHECK \= \[  
      "Parkside Dr",  
      "Garden Park dr",  
      \# Add more street names here  
  \]

* **BASE\_URL**: The base URL for the county's property search. This is already set but can be changed if the website's URL updates.  
* **DATA\_FILE\_PATH**: The name of the JSON file where property data will be stored. Defaults to property\_owners.json.

## **🏃 Usage**

Once configured, run the main script from your terminal:

python main.py

The script will:

1. Fetch data for each specified street.  
2. If it's the first run, it will save the scraped data to property\_owners.json.  
3. On subsequent runs, it will compare the new data with the existing property\_owners.json file.  
4. Print a summary of any **changes detected** (new properties, removed properties, or changes in owner/address for existing properties).  
5. Prompt you to confirm if you want to **overwrite** the local data file with the new data.

## **🔍 How Change Detection Works**

The script maintains a local property\_owners.json file. When you run main.py:

* It scrapes the current data and structures it as a dictionary where **parcel numbers are keys**, and the values are nested dictionaries containing the **owner's name** and **property address**.  
* It loads the previous\_properties from the JSON file.  
* It then performs a comparison:  
  * Checks if the owner\_name or address has changed for any existing parcel.  
  * Identifies any new properties (parcels present in the current data but not in the old data).  
  * Identifies any removed properties (parcels present in the old data but no longer found in the current scrape).  
* Finally, it presents these changes and asks for your confirmation to update the local data file.