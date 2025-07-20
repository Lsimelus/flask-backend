import csv


def format_string(text):
  """Converts a string to lowercase and replaces spaces with hyphens."""
  text = text.lower()
  text = text.replace(" ", "-")
  return text

OUTPUT_FILE = "result.csv"
rate_mapper = {}
PROPERTY_TAX_AND_COUNTY = "property_tax_county.csv"
with open(PROPERTY_TAX_AND_COUNTY, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=",")
    rate_mapper = {}
    for line in csv_reader:
        if line["State"] in rate_mapper:
            state = rate_mapper[line["State"]]
            state[line["County"].lower()] = {
                "median_value": line["Median Housing Value, 2023 ($)"],
                "median_tax": line["Effective Property Tax Rate (2023)"].strip("%")
            }
        else:
            rate_mapper[line["State"]] = {}
            rate_mapper[line["State"]][line["County"].lower()] = {
                "median_value": line["Median Housing Value, 2023 ($)"],
                "median_tax": line["Effective Property Tax Rate (2023)"].strip("%")
            }
        

CITY_STATE_COUNTY ="city_state_county.csv"
data = {} 

with open(CITY_STATE_COUNTY, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter="|")
    
    data = {}
    for line in csv_reader:
        if line["State full"] in data:
            state = data[line["State full"]]
            state[line["City"]] = {"county": line["County"].lower()}
        else:
            data[line["State full"]] = {line["City"]:{"county": line["County"].lower()} }
            

        if line["State full"] in rate_mapper:
            state_mapper = rate_mapper[line["State full"]]
        
            curr_city = data[line["State full"]][line["City"]]
            curr_county = curr_city["county"]
            
            if curr_county in state_mapper:
                curr_city.update(state_mapper[curr_county])
            elif curr_county+" county"  in state_mapper:
                curr_city.update(state_mapper[curr_county+" county"])

         
                                
providences_to_remove = ['Marshall Islands', 'Northern Mariana Islands', 'Federated States of Micronesia', 'Palau', 'Guam', 'American Samoa', 'US Armed Forces Pacific', 'US Armed Forces Europe', 'Washington, D.C.', 'Puerto Rico', 'Virgin Islands']
for key in providences_to_remove:
    data.pop(key, None)
    
with open(OUTPUT_FILE, 'w', newline='') as csvfile:
    fieldnames = ['state', 'city', 'county', 'median_value', 'median_tax']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=",")

    writer.writeheader()
    
    for state, cities_dict in data.items():
        for city, city_info in cities_dict.items():
            writer.writerow({
                fieldnames[0]: format_string(state),
                fieldnames[1]: format_string(city),
                fieldnames[2]: format_string(city_info["county"]),
                fieldnames[3]: city_info.get("median_value", ""),
                fieldnames[4]: city_info.get("median_tax", "")
            })
