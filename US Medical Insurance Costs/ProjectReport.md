# Project: US Medical Insurance Costs
### From: Codecademy
### By: Krutarth Ghuge 
#### Project Date: June 2024

## Description:
For this project, I investigated a medical insurance costs dataset in a .csv file (insurance.csv) using the Python skills that I have developed so far. This project was programmed using the Visual Studio Code editor and has been pushed to my Github repo.

## Project Goals:
1. To assess the data collected in the csv file based on the factors mentioned. 

2. How a factor affects the medical charges on the patient.

3. Does being healthy reduce medical charges?

4. More children = more bills?

5. Does your sex affect medical charges?


## Data:
The data available from the csv file (insurance.csv) -

Headers (for each person (entry)):
1. Age of person (numerical attribute): age
2. Sex (categorical attr. - male / female): sex
3. Body Mass Index (numerical attr.): bmi
4. Number of children (numerical attr.): children
5. Smoker (categorical attr. - yes / no): smoker
6. Region of th US the person resides (categorical attr. - Northwest, Northeast, Southeast, Southwest): region
7. Medical charges on insurance (numerical attr.): charges

Entries:
There are a total of 1338 data entries (people) whose data is collected into this csv file.

Points to note:
1. There is no missing data.
2. There are seven columns.
3. Some columns are numerical while some are categorical.


## Analysis:
I have performed some basic and intermediate analysis on the given data. 
From the dataset, is it possible to conduct various number of analysis ranging from the use of just one attribute to all of them. For this project, I am performing (writing) few functions or doing mathematical calculations to analyze and further visualize my findings.

Our data with highest interest is the charges column which is the ultimate base of this research file (most analysis includes this column).

Analysis that I performed:
1. Whether smokers have higher medical charges than non-smokers.

2. How the medical charges change with age.

3. How BMI across different regions of the US affect medical charges.

4. Trend between number of children of person and medical charges. 

5. Do males or females have higher charges.


## Evaluation:
1. Whether smokers have higher medical charges than non-smokers.
Data calculated:
    - The total number of people in dataset = 1338
    - Total number of males and females = 676, 662 respectively
    - Total number of smokers and non-smokers = 274, 1064 respectively
    - Total number of male smokers and female smokers = 159, 115 respectively
    - The total medical charges = $17,755,824.99
    - The total medical charges for smokers and non-smokers = $8781763.52, $8974061.47 respectively
    - The average charges for smokers and non-smokers = $32050.23, $8434.27 respectively


For this finding, I went deep to find out all the small scale calculations part required for this analysis. The analysis turned out to be more mathematical than programmable.

Concluding with our findings, the results show that smokers had a higher average medical charge than the non-smokers. Although the total charges for each group were near about the same, due to a small number of smokers in the dataset, their average charge soared.


2. How the medical charges change with age.
    Comprising data:<br>
    - Total charge per age<br>
    - Age with max charges<br>
    - Age with min charges<br>
    - Age with highest average charges<br>
    - Age with lowest average charges

3. How BMI across different regions of the US affect medical charges.
    Comprising data:<br>
    - Total charge per bmi<br>
    - BMI with max charges<br>
    - BMI with min charges<br>
    - Regions with highest/lowest average BMI<br>
    - Average charges in each region<br>
    - Average charges per BMI range
    (<18.5: Underweight, 18.5 < BMI < 24.9: Healthy weight, 25.0 < BMI < 29.9: Overweight, >30.0: Obesity)<br>
    - Average charges per BMI range in every region

4. Trend between number of children of person and medical charges. 
    Comprising data:<br>
    - Total people with different num of children<br>
    - Average charge for each group (num of children)<br>
    - Minimum charge for each num of children<br>
    - Maximum charge for each num of children<br>
    - Person's sex and number of children<br>
    - Charges for each sex with different num of children

5. Do males or females have higher charges.<br>
    Comprising data:<br>
    - Total males<br>
    - Total females<br>
    - Min/max charge for each<br>
    - Average charge for each

## Outputs:

### Analysis 1
![Analysis 1 Output](/img/analysis1.png)


## Further study:


## Resources and Links:
1. Overview, Instructions and Setup: 
    https://www.codecademy.com/projects/portfolio/us-medical-insurance-costs-portfolio-project

2. Dataset:
    https://www.kaggle.com/datasets/mirichoi0218/insurance 

3. BMI:
    https://www.cdc.gov/healthyweight/assessing/bmi/adult_bmi/index.html 

