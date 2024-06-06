#################################################################################################################

################################################## CAUTION ##################################################
# DO NOT ATTEMPT TO RUN FILE WITH ALL ANALYSIS UNCOMMENTED
# PROCESS WILL TAKE LOT OF PROCESSING POWER AND MAY DAMAGE YOUR DEVICE (CODE IS NOT FULLY OPTIMIZED)
# RUN EACH ANALYSIS SEPARATE
# THIS PROGRAM IS NOT CODE-OPTIMIZED AS I HAVE JUST WRITTEN IT FOR MY FIRST INDEPENDENT PORTFOLIO PROJECT
#################################################################################################################

################################################## START OF FILE ##################################################


# Refer to Project Webpage for Project Report
# Written by Krutarth Ghuge

#################################################################################################################
#################################################################################################################
#################################################################################################################

################################################## LOADING ##################################################

import csv
from decimal import Decimal
import matplotlib.pyplot as plt


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

### Separated data for each column
ageHeader = headers[0] # Retrieving header for age data column
rawAgeData = columns_data[ageHeader] # List of age data
ageData = [int(item) for item in rawAgeData]
sexHeader = headers[1] # Retrieving header for sex data column
sexData = columns_data[sexHeader] # List of sex data
bmiHeader = headers[2] #  Retrieving header for bmi data column
rawBmiData = columns_data[bmiHeader] # List of bmi data
bmiData = [Decimal(item) for item in rawBmiData]
childrenHeader = headers[3] # Retrieving header of number of children data column
strChildrenData = columns_data[childrenHeader] # List of number of children data
childrenData = [int(item) for item in strChildrenData]
smokingHeader = headers[4] # Retrieving header for smoking data column
smokingData = columns_data[smokingHeader] # List of smoking data
regionHeader = headers[5] # Retrieving header for US region data column
regionData = columns_data[regionHeader] # List of US regions data
chargesHeader = headers[6] # Retrieving header for medical charges data column
rawChargesData = columns_data[chargesHeader] # List of medical charges data
chargesData = [float(item) for item in rawChargesData]


# Now, columns_data dictionary contains lists for each column
# Prints out all the data column-wise
# You can access the arrays for each column like this:
'''
for header, data in columns_data.items():
    print(f"{header}: {data}")
'''

################################################## START OF ANALYSIS 1 ##################################################

## Whether smokers have higher medical charges than non-smokers

# Introduction
print("\nIn this section, we are analyzing whether smokers or non-smokers have higher medical charges across the US.\n")

# Variables to hold counts
males = 0  # Variable to hold the number of males

# Calculating the number of males and hence females
for i in sexData:
    if i == "male":
        males += 1
females = totalDataLength - males  # Number of females
print(f"Total males: {males}, total females: {females}")

# Find charges for each sex
totalChargesMale = 0
for i in range(totalDataLength):
    if sexData[i] == "male":
        totalChargesMale += chargesData[i]
totalChargesFemale = 0
for i in range(totalDataLength):
    if sexData[i] == "female":
        totalChargesFemale += chargesData[i]

# Calculating average charges for males and females
avgChargeMales = totalChargesMale / males
avgChargeFemales = totalChargesFemale / females
print(f"Average medical charges for males = ${avgChargeMales}, and for females = ${avgChargeFemales}")

# Find total number of smokers
totalSmokers = 0  # Variable to hold the number of smokers

# Calculating the number of smokers
for i in smokingData:
    if i == "yes":
        totalSmokers += 1
nonSmokers = totalDataLength - totalSmokers  # Total number of non-smokers
print(f"The total number of smokers is {totalSmokers}, hence non-smokers are {nonSmokers}")

# Variables to hold counts
maleSmokers = 0  # Holds number of male smokers
femaleSmokers = 0  # Holds number of female smokers

# Calculating number of male smokers and female smokers
for i in range(totalDataLength):
    if sexData[i] == "male" and smokingData[i] == "yes":
        maleSmokers += 1
    elif sexData[i] == "female" and smokingData[i] == "yes":
        femaleSmokers += 1
print(f"Number of male smokers: {maleSmokers}, number of female smokers: {femaleSmokers}")

# Variables to hold total charges
totalCharges = 0  # Variable to hold total medical charges

# Calculating total medical charges across all regions of the US
for charge in chargesData:
    totalCharges += float(charge)
print(f"The total medical charges are ${totalCharges:.2f}")

# Variables to hold charges for smokers and non-smokers
smokersCharges = 0
for i in range(totalDataLength):
    if smokingData[i] == "yes":
        smokersCharges += float(chargesData[i])

nonSmokersCharges = totalCharges - smokersCharges
averageSmokersCharges = smokersCharges / totalSmokers
averageNonSmokerCharges = nonSmokersCharges / nonSmokers

# Printing results
print(f"Total charges for smokers: ${smokersCharges:.2f}")
print(f"Total charges for non-smokers: ${nonSmokersCharges:.2f}")
print(f"The average charges for smokers is: ${averageSmokersCharges:.2f}")
print(f"The average charges for non-smokers is: ${averageNonSmokerCharges:.2f}\n\n")


################################################## END OF ANALYSIS 1 ##################################################

################################################## START OF ANALYSIS 2 ##################################################

## How the medical charges change with age
# Introduction
#print("\nIn this section, we are analyzing how the medical charges vary with age.\n")

# Function to find the highest medical charge and its corresponding age
def getHighestCharge():
    maxValue = max(chargesData)
    getIndex = chargesData.index(maxValue)
    return maxValue, getIndex

# Function to find the lowest medical charge and its corresponding age
def getLowestCharge():
    minValue = min(chargesData)
    getIndex = chargesData.index(minValue)
    return minValue, getIndex

# Function to get total charges for each age
def getTotalChargesPerAge():
    maxAge = max(ageData)
    newAgeList = list(range(maxAge + 1))
    totalsPerAge = [0] * (maxAge + 1)
    for i in range(totalDataLength):
        ageOfEntry = ageData[i]
        totalsPerAge[ageOfEntry] += chargesData[i]
    return newAgeList, totalsPerAge

# Function to calculate average charges for each age
def getAverageChargesPerAge():
    maxAge = max(ageData)
    newAgeList = list(range(maxAge + 1))
    avgsPerAge = [0] * (maxAge + 1)
    ageCount = [0] * (maxAge + 1)
    for i in range(totalDataLength):
        ageOfEntry = ageData[i]
        ageCount[ageOfEntry] += 1
    for i in range(maxAge + 1):
        if ageCount[i] != 0:
            avgsPerAge[i] = getTotalChargesPerAge()[1][i] / ageCount[i]
        else:
            avgsPerAge[i] = 0
    return newAgeList, avgsPerAge

# Function to find the age with the highest average charge
def getHighestAvgCharge():
    highestAvg = max(getAverageChargesPerAge()[1])
    ageWithHighestAvg = getAverageChargesPerAge()[1].index(highestAvg)
    return highestAvg, ageWithHighestAvg

# Function to find the age with the lowest average charge
def getLowestAvgCharge():
    lowestAvg = None
    for num in getAverageChargesPerAge()[1]:
        if num != 0:
            if lowestAvg is None or num < lowestAvg:
                lowestAvg = num
    ageWithLowestAvg = getAverageChargesPerAge()[1].index(lowestAvg)
    return lowestAvg, ageWithLowestAvg

## Checking whether the written functions work

# Printing the age with the highest and lowest total medical charges
print(f"The age with the highest charge ${getHighestCharge()[0]:.2f} is {ageData[getHighestCharge()[1]]}\n")
getHighestCharge()  # printing the age with the highest total medical charges
print(f"The age with the lowest charge ${getLowestCharge()[0]:.2f} is {ageData[getLowestCharge()[1]]}\n")
getLowestCharge()  # printing the age with the lowest total medical charges
print()

# Printing the total charges and the average charges for each age
for i in range(len(getTotalChargesPerAge()[1])):
    if getTotalChargesPerAge()[1][i] != 0:
        print(f"The total charges for age: {getTotalChargesPerAge()[0][i]} are ${getTotalChargesPerAge()[1][i]:.2f}")
        print(f"The average medical charges for age: {getAverageChargesPerAge()[0][i]} are ${getAverageChargesPerAge()[1][i]:.2f}")

print()

# Printing the ages with the highest average and lowest average charge
print(f"The highest average charge is ${getHighestAvgCharge()[0]:.2f} for the age {getHighestAvgCharge()[1]}\n")
print(f"The lowest average charge is ${getLowestAvgCharge()[0]:.2f} for the age {getLowestAvgCharge()[1]}\n")

# Creating a line graph plot
# The graph has two lines - one showing total charges for each age, the other showing the average charge

# Data
x1 = getAverageChargesPerAge()[0]  # x-axis showing ages
y2 = getAverageChargesPerAge()[1]  # line 2 showing averages for each age

# Plot the line graph
plt.figure()  # Create another new figure
plt.plot(x1, y2, label='Average Charges', color='red')
plt.xlabel('Age')
plt.ylabel('Average Charges ($)')
plt.title('Average Charges')
plt.legend()

# Display the plots
plt.show()

################################################## END OF ANALYSIS 2 ##################################################

################################################## START OF ANALYSIS 3 ##################################################
## 3. How BMI across different regions of the US affect medical charges

# Function to categorize BMI into different categories
# Namely - underweight, healthy-weight, overweight, obesity
# If the BMI falls under that category, the value is changed to True in that specific array at that person's index
def bmiDistribution():
    underWeight = [False] * totalDataLength
    healthyWeight = [False] * totalDataLength
    overWeight = [False] * totalDataLength
    obesity = [False] * totalDataLength
    for i in range(totalDataLength):
        if bmiData[i] < 18.5:
            underWeight[i] = True
        elif 18.5 <= bmiData[i] <= 24.9:
            healthyWeight[i] = True
        elif 25.0 <= bmiData[i] <= 29.9:
            overWeight[i] = True
        else:
            obesity[i] = True
    return underWeight, healthyWeight, overWeight, obesity

# Function to calculate the number of people in every BMI range
def getBmiDistributionCount():
    underWeightCount = healthyWeightCount = overWeightCount = obesityCount = 0
    for i in range(totalDataLength):
        if bmiDistribution()[0][i] == True:
            underWeightCount += 1
        elif bmiDistribution()[1][i] == True:
            healthyWeightCount += 1
        elif bmiDistribution()[2][i] == True:
            overWeightCount += 1
        elif bmiDistribution()[3][i] == True:
            obesityCount += 1
    return underWeightCount, healthyWeightCount, overWeightCount, obesityCount       

# Get the index of the person with the highest and lowest medical charges
highestBmiIndex = chargesData.index(getHighestCharge()[0])
lowestBmiIndex = chargesData.index(getLowestCharge()[0])
print(f"\nThe BMI with the highest medical charge is {bmiData[highestBmiIndex]}")
print(f"The BMI with the lowest medical charge is {bmiData[lowestBmiIndex]}\n")

# Calculate the total charges for each BMI range
underWeightTotal = healthyWeightTotal = overWeightTotal = obesityTotal = 0.0
for i in range(totalDataLength):
    if bmiDistribution()[0][i] == True:
        underWeightTotal += chargesData[i]
    elif bmiDistribution()[1][i] == True:
        healthyWeightTotal += chargesData[i]
    elif bmiDistribution()[2][i] == True:
        overWeightTotal += chargesData[i]
    elif bmiDistribution()[3][i] == True:
        obesityTotal += chargesData[i]

# Calculate averages for each BMI range
avgChargeUnderWeight = underWeightTotal / getBmiDistributionCount()[0]
avgChargeHealthyWeight = healthyWeightTotal / getBmiDistributionCount()[1]
avgChargeOverWeight = overWeightTotal / getBmiDistributionCount()[2]
avgChargeObesity = obesityTotal / getBmiDistributionCount()[3]

print(f"The average charges for each BMI range are: \n Underweight = ${avgChargeUnderWeight:.2f}\n Healthy Weight = ${avgChargeHealthyWeight:.2f}\n Overweight = ${avgChargeOverWeight:.2f}\n Obesity = ${avgChargeObesity:.2f}\n")



# Function to distribute individuals based on their region of the US
def regionDistribution():
    northWest = [False] * totalDataLength
    northEast = [False] * totalDataLength
    southEast = [False] * totalDataLength
    southWest = [False] * totalDataLength
    for i in range(totalDataLength):
        if regionData[i] == "northwest":
            northWest[i] = True
        elif regionData[i] == "northeast":
            northEast[i] = True
        elif regionData[i] == "southeast":
            southEast[i] = True
        elif regionData[i] == "southwest":
            southWest[i] = True
    return northWest, northEast, southEast, southWest

# Function to calculate the number of people in every region of the US
def getRegionDistributionCount():
    northWestCount = northEastCount = southEastCount = southWestCount = 0
    for i in range(totalDataLength):
        if regionDistribution()[0][i] == True:
            northWestCount += 1
        elif regionDistribution()[1][i] == True:
            northEastCount += 1
        elif regionDistribution()[2][i] == True:
            southEastCount += 1
        elif regionDistribution()[3][i] == True:
            southWestCount += 1
    return northWestCount, northEastCount, southEastCount, southWestCount

# Calculate the total charges for each US region
northWestTotal = northEastTotal = southEastTotal = southWestTotal = 0.0
for i in range(totalDataLength):
    if regionDistribution()[0][i] == True:
        northWestTotal += chargesData[i]
    elif regionDistribution()[1][i] == True:
        northEastTotal += chargesData[i]
    elif regionDistribution()[2][i] == True:
        southEastTotal += chargesData[i]
    elif regionDistribution()[3][i] == True:
        southWestTotal += chargesData[i]

## Get averages
avgChargeNorthWest = northWestTotal / getRegionDistributionCount()[0]
avgChargeNorthEast = northEastTotal / getRegionDistributionCount()[1]
avgChargeSouthEast= southEastTotal / getRegionDistributionCount()[2]
avgChargeSouthWest = southWestTotal / getRegionDistributionCount()[3]

print(f"The average charges for each region are: \n NorthWest = ${avgChargeNorthWest:.2f}\n NorthEast = ${avgChargeNorthEast:.2f}\n SouthEast = ${avgChargeSouthEast:.2f}\n SouthWest = ${avgChargeSouthWest:.2f}\n")

## Plotting pie charts for each region showing distribution of BMI

# Function to get BMI distribution counts for each region
def getBmiDistributionCountForRegion(region):
    underWeightCount = healthyWeightCount = overWeightCount = obesityCount = 0
    regionDist = regionDistribution()
    bmiDist = bmiDistribution()
    
    for i in range(totalDataLength):
        if region[i]:
            if bmiDist[0][i]:
                underWeightCount += 1
            elif bmiDist[1][i]:
                healthyWeightCount += 1
            elif bmiDist[2][i]:
                overWeightCount += 1
            else:
                obesityCount += 1
    return underWeightCount, healthyWeightCount, overWeightCount, obesityCount

# Getting BMI distribution counts for each region
northWestDist = getBmiDistributionCountForRegion(regionDistribution()[0])
northEastDist = getBmiDistributionCountForRegion(regionDistribution()[1])
southEastDist = getBmiDistributionCountForRegion(regionDistribution()[2])
southWestDist = getBmiDistributionCountForRegion(regionDistribution()[3])

# Labels for the pie charts
labels = ['Underweight', 'Healthy Weight', 'Overweight', 'Obesity']

# Creating a figure with 2x2 subplots
fig, axes = plt.subplots(2, 2, figsize=(10, 10))

# Plotting the pie charts for each region
axes[0, 0].pie(northWestDist, labels=labels, autopct='%1.1f%%', startangle=90)
axes[0, 0].set_title('Northwest Region BMI Distribution')

axes[0, 1].pie(northEastDist, labels=labels, autopct='%1.1f%%', startangle=90)
axes[0, 1].set_title('Northeast Region BMI Distribution')

axes[1, 0].pie(southEastDist, labels=labels, autopct='%1.1f%%', startangle=90)
axes[1, 0].set_title('Southeast Region BMI Distribution')

axes[1, 1].pie(southWestDist, labels=labels, autopct='%1.1f%%', startangle=90)
axes[1, 1].set_title('Southwest Region BMI Distribution')

# Adjust layout to prevent overlap
plt.tight_layout()

# Display the pie charts
plt.show()


################################################## END OF ANALYSIS 3 ##################################################

################################################## START OF ANALYSIS 4 ##################################################

### Trend between number of children of person and medical charges


# Function to count the number of individuals based on the number of children they have
def countNumChildren():
    noChildrenCount = oneChildCount = twoChildrenCount = threeChildrenCount = fourChildrenCount = fiveChildrenCount = 0
    for i in range(totalDataLength):
        if childrenData[i] == 0:
            noChildrenCount += 1
        elif childrenData[i] == 1:
            oneChildCount += 1
        elif childrenData[i] == 2:
            twoChildrenCount += 1
        elif childrenData[i] == 3:
            threeChildrenCount += 1
        elif childrenData[i] == 4:
            fourChildrenCount += 1
        elif childrenData[i] == 5:
            fiveChildrenCount += 1
    return noChildrenCount, oneChildCount, twoChildrenCount, threeChildrenCount, fourChildrenCount, fiveChildrenCount

# Print the counts for each number of children
print(f"\nTotal people with no children = {countNumChildren()[0]}, one child = {countNumChildren()[1]}, two children = {countNumChildren()[2]}")
print(f"Three children = {countNumChildren()[3]}, four children = {countNumChildren()[4]}, and five children = {countNumChildren()[5]}")

# Function to calculate the average medical charge for individuals based on the number of children they have
def avgChargeNumChildren():
    zeroChildrenTotal = oneChildTotal = twoChildrenTotal = threeChildrenTotal = fourChildrenTotal = fiveChildrenTotal = 0
    for i in range(totalDataLength):
        if childrenData[i] == 0:
            zeroChildrenTotal += chargesData[i]
        elif childrenData[i] == 1:
            oneChildTotal += chargesData[i]
        elif childrenData[i] == 2:
            twoChildrenTotal += chargesData[i]
        elif childrenData[i] == 3:
            threeChildrenTotal += chargesData[i]
        elif childrenData[i] == 4:
            fourChildrenTotal += chargesData[i]
        elif childrenData[i] == 5:
            fiveChildrenTotal += chargesData[i]
    avgZeroChildCharges = zeroChildrenTotal / countNumChildren()[0]
    avgOneChildCharges = oneChildTotal / countNumChildren()[1]
    avgTwoChildCharges = twoChildrenTotal / countNumChildren()[2]
    avgThreeChild = threeChildrenTotal / countNumChildren()[3]
    avgFourChild = fourChildrenTotal / countNumChildren()[4]
    avgFiveChild = fiveChildrenTotal / countNumChildren()[5]
    return avgZeroChildCharges, avgOneChildCharges, avgTwoChildCharges, avgThreeChild, avgFourChild, avgFiveChild

# Print the average charges for each number of children
print(f"\nAverage medical charge for people with no children = ${avgChargeNumChildren()[0]:.2f}, one child = ${avgChargeNumChildren()[1]:.2f}, two children = ${avgChargeNumChildren()[2]:.2f}")
print(f"Three children = ${avgChargeNumChildren()[3]:.2f}, four children = ${avgChargeNumChildren()[4]:.2f}, and five children = ${avgChargeNumChildren()[5]:.2f}\n")

# Function to find the maximum medical charge for individuals with a specified number of children
def findMaxCharge(numOfChildren):
    chargesNumChildren = []
    for i in range(totalDataLength):
        if childrenData[i] == numOfChildren:
            chargesNumChildren.append(chargesData[i])
    maxCharge = max(chargesNumChildren)
    return maxCharge

# Function to find the minimum medical charge for individuals with a specified number of children
def findMinCharge(numOfChildren):
    chargesNumChildren = []
    for i in range(totalDataLength):
        if childrenData[i] == numOfChildren:
            chargesNumChildren.append(chargesData[i])
    minCharge = min(chargesNumChildren)
    return minCharge

# Testing to find min and max medical charges for people with a certain number of children
user_input_max = int(input("Enter to find max medical charges for people with this number of children: "))
user_input_min = int(input("Enter to find min medical charges for people with this number of children: "))

maxCharge_user_input = findMaxCharge(user_input_max)
minCharge_user_input = findMinCharge(user_input_min)
print(f"The maximum charge for people with {user_input_max} children = ${maxCharge_user_input:.2f}")
print(f"The minimum charge for people with {user_input_min} children = ${minCharge_user_input:.2f}\n")

# Sample data for plotting
x_axis = []
y_axis = []
for i in range(max(childrenData)+ 1):
    x_axis.append(i)
    y_axis.append(avgChargeNumChildren()[i])

# Plotting the bar chart
plt.bar(x_axis, y_axis, color='blue', edgecolor='black')

# Adding title and labels
plt.title('Average medical charge per number of children')
plt.xlabel('Number of Children')
plt.ylabel('Average Medical Charge ($)')

# Display the bar chart
plt.show()


################################################## END OF ANALYSIS 4 ##################################################


#################################################################################################################
#################################################################################################################
#################################################################################################################
################################################## END OF FILE ##################################################