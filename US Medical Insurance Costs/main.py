# Refer to ReadMe.md for project details
# Written by Krutarth Ghuge

################################################## LOADING ##################################################

import csv

# Define the file name
filename = 'starterFiles/insurance.csv'

# Initialize a dictionary to hold lists for each column
columns_data = {}

# Read the CSV file
with open(filename, mode='r') as file:
    csv_reader = csv.reader(file)
    headers = next(csv_reader)  # Read the header row
    
    # Initialize lists for each header
    for header in headers:
        columns_data[header] = []
    
    # Read the rows and append the data to the corresponding header list    
    for row in csv_reader:
        for i, header in enumerate(headers):
            columns_data[header].append(row[i])

totalDataLength = len(columns_data[header]) # the total data entries in our file

# Now, columns_data dictionary contains lists for each column
# Prints out all the data column-wise
# You can access the arrays for each column like this:
'''
for header, data in columns_data.items():
    print(f"{header}: {data}")

'''

################################################## START OF ANALYSIS 1 ##################################################

# Whether smokers have higher medical charges than non-smokers

print("\nIn this section we are trying to find whether smokers or non-smokers have higher medical charges across the US\n")

sexHeader = headers[1] # Retrieving header for sex data column
sexData = columns_data[sexHeader] # List of sex data
males = 0 # variable to hold number of males

# calculating number of males and hence females
for i in sexData:
    if i == "male":
        males = males + 1   

females = totalDataLength - males # number of females
print(f"Total males: {males}, total females: {females}")

# Find total number of smokers
smokingHeader = headers[4] # Retrieving header for smoking data column
smokingData = columns_data[smokingHeader] # List of smoking data
totalSmokers = 0 # variable to hold number of smokers

# calculating number of smokers
for i in smokingData:
    if i == "yes":
        totalSmokers = totalSmokers + 1
        
nonSmokers = totalDataLength - totalSmokers # total number of non-smokers
print(f"The total number of smokers is {totalSmokers}, hence non smokers are {nonSmokers}")


maleSmokers = 0 # holds number of male smokers
femaleSmokers = 0 # holds number of female smokers

# calculating number of male smokers and female smokers
for i in range(0, totalDataLength, 1):
    if sexData[i] == "male" and smokingData[i] == "yes":
        maleSmokers = maleSmokers + 1
    elif sexData[i] == "female" and smokingData[i] == "yes":
        femaleSmokers = femaleSmokers + 1

print(f"Number of male smokers: {maleSmokers}, number of female smokers: {femaleSmokers}")


chargesHeader = headers[6] # Retrieving header for medical charges data column
chargesData = columns_data[chargesHeader] # List of medical charges data
totalCharges = 0 # variable to hold total medical charges

# calculating total medical charges across all regions of the US
for charge in chargesData:
    totalCharges = totalCharges + float(charge)
print(f"The total medical charges are ${totalCharges:.2f}")

smokersCharges = 0


for i in range(0, totalDataLength, 1):
    if smokingData[i] == "yes":
        smokersCharges = smokersCharges + float(chargesData[i])

nonSmokersCharges = totalCharges - smokersCharges
averageSmokersCharges = smokersCharges / totalSmokers
averageNonSmokerCharges = nonSmokersCharges / nonSmokers

print(f"Total charges for smokers: ${smokersCharges:.2f}")
print(f"Total charges for non-smokers: ${nonSmokersCharges:.2f}")
print(f"The average charges for smokers is: ${averageSmokersCharges:.2f}")
print(f"The average charges for non smokers is: ${averageNonSmokerCharges:.2f}\n\n")


################################################## END OF ANALYSIS 1 ##################################################


################################################## START OF ANALYSIS 2 ##################################################



################################################## END OF ANALYSIS 2 ##################################################


################################################## START OF ANALYSIS 3 ##################################################



################################################## END OF ANALYSIS 3 ##################################################


################################################## START OF ANALYSIS 4 ##################################################



################################################## END OF ANALYSIS 4 ##################################################


################################################## START OF ANALYSIS 5 ##################################################



################################################## END OF ANALYSIS 5 ##################################################







