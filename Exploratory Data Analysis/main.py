#############################################################################################################################
# Iteration 2 of the original file for the EDA Project
# Lesser code
# More efficient

########################################################## UNDER WORK ##########################################################
########################################################## LOADING ##########################################################

import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, box
import math
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from decimal import Decimal
from pandas.api.types import CategoricalDtype

########################################################## MENU OPTION 1 ##########################################################

def is_within_grid_corrected(center_lat, center_lon, point_lat, point_lon, grid_size_km):
    """
    Check if a point (point_lat, point_lon) is within a grid centered at (center_lat, center_lon) with a specified size.
    """
    # Calculate the degrees per kilometer for latitude and longitude
    km_per_deg_lat = 111.0
    km_per_deg_lon = 111.0 * math.cos(math.radians(center_lat))
    
    # Calculate the bounding box of the grid
    lat_min = center_lat - (grid_size_km / (2 * km_per_deg_lat))
    lat_max = center_lat + (grid_size_km / (2 * km_per_deg_lat))
    lon_min = center_lon - (grid_size_km / (2 * km_per_deg_lon))
    lon_max = center_lon + (grid_size_km / (2 * km_per_deg_lon))
    
    # Check if the point is within the grid
    within_grid = lat_min <= point_lat <= lat_max and lon_min <= point_lon <= lon_max
    
    # Print results and bounding box details
    if within_grid:
        print(f"\nThe point ({point_lat}, {point_lon}) is within the {grid_size_km} km grid centered at ({center_lat}, {center_lon}).\n")
    else:
        print(f"\nThe point ({point_lat}, {point_lon}) is NOT within the {grid_size_km} km grid centered at ({center_lat}, {center_lon}).\n")
    
    print(f"Bounding box for the {grid_size_km} km grid centered at ({center_lat}, {center_lon}):")
    print(f"Latitude range: {lat_min} to {lat_max}")
    print(f"Longitude range: {lon_min} to {lon_max}")
    
    return within_grid

########################################################## MENU OPTION 2 ##########################################################

def calculate_emissions_profiles(file_path):
    """
    Calculate emissions profiles for aggregated grid cells over multiple years, specified by the user.
    """
    df = pd.read_csv(file_path)

    # Convert start_time to year if available, otherwise use the year column directly
    if 'start_time' in df.columns and 'end_time' in df.columns:
        df['year'] = pd.to_datetime(df['start_time']).dt.year
    else:
        df['year'] = df['year']

    # Create a GeoDataFrame with the geometry of points
    geometry = [Point(xy) for xy in zip(df.lon, df.lat)]
    gdf = gpd.GeoDataFrame(df, geometry=geometry)

    # Get user inputs for the grid cell definition
    cell_x_min = float(input("Enter the minimum longitude of the starting grid cell: "))
    cell_y_min = float(input("Enter the minimum latitude of the starting grid cell: "))
    cell_size_km = float(input("Enter the grid cell size in km: "))
    
    # Calculate the size of the cell in degrees
    km_per_deg_lat = 111.0
    km_per_deg_lon = 111.0 * math.cos(math.radians(cell_y_min))
    cell_size_deg_lat = cell_size_km / km_per_deg_lat
    cell_size_deg_lon = cell_size_km / km_per_deg_lon

    # Define the bounding box for the grid cell
    max_lat = cell_y_min + cell_size_deg_lat
    max_lon = cell_x_min + cell_size_deg_lon
    initial_cell = box(cell_x_min, cell_y_min, max_lon, max_lat)
    initial_cell_gdf = gpd.GeoDataFrame([initial_cell], columns=['geometry'])

    # Get user input for the years of interest
    years_of_interest_str = input("Enter the list of years of interest (comma-separated): ")
    years_of_interest = [int(year.strip()) for year in years_of_interest_str.split(',')]

    # Initialize dictionary to store emissions profiles
    emissions_profiles = {year: {} for year in years_of_interest}

    for year in years_of_interest:
        # Filter data for the specific year
        yearly_data = gdf[gdf['year'] == year]
        # Join data with the grid cell to get emissions within the cell
        joined_cell = gpd.sjoin(yearly_data, initial_cell_gdf, how='inner', predicate='within')
        
        if not joined_cell.empty:
            # Sum emissions for each gas
            cell_emissions = joined_cell.groupby('gas')['emissions_quantity'].sum()
            emissions_profiles[year][f'Cell: {cell_x_min}, {cell_y_min}'] = cell_emissions

    # Print the emissions profiles
    for year, profiles in emissions_profiles.items():
        print(f"\nEmissions Profiles for {year}:")
        for cell, profile in profiles.items():
            print(f"\n{cell}:")
            for gas, quantity in profile.items():
                print(f"{gas}: {quantity} Metric Tonnes")

########################################################## MENU OPTION 3 ##########################################################

def plot_total_emissions_by_sector_and_gas():
    """
    Plot total greenhouse gas emissions by sector for a specified year and gas.
    """
    file_path = input("\nEnter the path to the emissions CSV file: ")  # Prompt user to input file path

    try:
        # Load the data from CSV file
        df = pd.read_csv(file_path)
        
        # Replace infinite values with NaN
        df.replace([np.inf, -np.inf], np.nan, inplace=True)
        
        # Fill NaN values with appropriate values based on column type
        for col in df.columns:
            if df[col].dtype == 'object':
                df[col].fillna('NA', inplace=True)  # Fill NaNs in object type columns with 'NA'
            else:
                df[col].fillna(0, inplace=True)  # Fill NaNs in numeric columns with 0

        # Convert specific columns to numeric type, coercing errors to NaN
        df['co2'] = pd.to_numeric(df['co2'], errors='coerce')
        df['ch4'] = pd.to_numeric(df['ch4'], errors='coerce')
        df['n2o'] = pd.to_numeric(df['n2o'], errors='coerce')
        df['co2e_100yr'] = pd.to_numeric(df['co2e_100yr'], errors='coerce')
        df['co2e_20yr'] = pd.to_numeric(df['co2e_20yr'], errors='coerce')

        # Mapping of subsectors to sectors
        sectors_mapping = {
            'agriculture': ['cropland-fires', 'enteric-fermentation-cattle-feedlot', 'enteric-fermentation-cattle-pasture', 'enteric-fermentation-other', 'manure-left-on-pasture-cattle', 'manure-management-cattle-feedlot', 'manure-management-other', 'other-agricultural-soil-emissions', 'rice-cultivation', 'synthetic-fertilizer-application'],
            'buildings': ['residential-and-commercial-onsite-fuel-usage', 'other-onsite-fuel-usage'],
            'fluorinatedGases': ['fluorinated-gases'],
            'fossilFuelOperations': ['coal-mining', 'oil-and-gas-production-and-transport', 'oil-and-gas-refining', 'other-fossil-fuel-operations', 'solid-fuel-transformation'],
            'forestryAndLandUse': ['shrubgrass-fires', 'removals', 'forest-land-fires', 'wetland-fires', 'forest-land-degradation', 'net-shrubgrass', 'forest-land-clearing', 'net-forest-land', 'net-wetland', 'water-reservoirs'],
            'manufacturing': ['aluminum', 'steel', 'cement', 'petrochemicals', 'chemicals', 'other-manufacturing', 'pulp-and-paper'],
            'mineralExtraction': ['bauxite-mining', 'copper-mining', 'iron-mining', 'rock-quarrying', 'sand-quarrying'],
            'power': ['electricity-generation', 'other-energy-use'],
            'transportation': ['domestic-aviation', 'domestic-shipping', 'international-aviation', 'international-shipping', 'other-transport', 'railways', 'road-transportation'],
            'waste': ['biological-treatment-of-solid-waste-and-biogenic', 'incineration-and-open-burning-of-waste', 'solid-waste-disposal', 'wastewater-treatment-and-discharge']
        }

        # Function to determine sector based on subsector
        def get_sector(subsector):
            for sector, subsectors in sectors_mapping.items():
                if subsector in subsectors:
                    return sector
            return 'Unknown'

        # Add a 'sector' column based on 'sub_sector' values using the get_sector function
        df['sector'] = df['sub_sector'].apply(get_sector)

        # Prompt user to input the year of interest for greenhouse gas distributions
        year = int(input("Enter the year for which you want the greenhouse gas distributions (e.g., 2020): "))

        # Function to plot total emissions by sector for each greenhouse gas of interest
        def plot_total_emissions_by_sector(df, gas, year):
            # Filter data for the specified year
            df_year = df[df['year'] == year]
            
            # Calculate total emissions by sector for the specified greenhouse gas
            total_emissions = df_year.groupby('sector')[gas].sum().reset_index()
            
            # Plot the data
            plt.figure(figsize=(14, 8))
            sns.barplot(data=total_emissions, x='sector', y=gas, palette='tab20')
            plt.title(f'Total {gas} Emissions by Sector in {year}')
            plt.xlabel('Sector')
            plt.ylabel(f'Total {gas} Emissions')
            plt.xticks(rotation=45)

            # Add text labels to each bar in the plot
            for index, row in total_emissions.iterrows():
                plt.text(index, row[gas], f'{row[gas]:.2f}', color='black', ha="center")

            plt.show()

        # Loop through each greenhouse gas of interest and plot emissions by sector
        for gas in ['co2', 'ch4', 'n2o', 'co2e_100yr', 'co2e_20yr']:
            plot_total_emissions_by_sector(df, gas, year)

    except FileNotFoundError:
        print(f"Error: The file at path '{file_path}' was not found.")  # Handle file not found error
    except ValueError as ve:
        print(f"Error: {ve}")  # Handle value error
    except Exception as e:
        print(f"An unexpected error occurred: {e}")  # Handle unexpected errors

########################################################## MENU OPTION 4 ##########################################################

# Function to plot total emissions by subsector for a specified greenhouse gas
def plot_total_emissions_by_subsector(file_path, gas):
    """
    Plot total emissions by subsector for a specified gas.

    Parameters:
    - file_path: Path to the emissions CSV file.
    - gas: String indicating the type of greenhouse gas (e.g., 'co2', 'ch4', 'n2o', 'co2e_100yr', 'co2e_20yr').
    """
    # Read data from CSV file into DataFrame
    df = pd.read_csv(file_path)
    
    # Replace infinite values with NaN
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    
    # Fill NaN values with 0
    df.fillna(0, inplace=True)

    # Convert specific columns to numeric type, coercing errors to NaN
    df['co2'] = pd.to_numeric(df['co2'], errors='coerce')
    df['ch4'] = pd.to_numeric(df['ch4'], errors='coerce')
    df['n2o'] = pd.to_numeric(df['n2o'], errors='coerce')
    df['co2e_100yr'] = pd.to_numeric(df['co2e_100yr'], errors='coerce')
    df['co2e_20yr'] = pd.to_numeric(df['co2e_20yr'], errors='coerce')

    # Group by subsector and sum emissions for the specified gas
    total_emissions = df.groupby('sub_sector')[gas].sum().reset_index()
    
    # Plot the data
    plt.figure(figsize=(14, 8))
    sns.barplot(data=total_emissions, x='sub_sector', y=gas, palette='tab20')
    plt.title(f'Total {gas} Emissions by Subsector')
    plt.xlabel('Subsector')
    plt.ylabel(f'Total {gas} Emissions')
    plt.xticks(rotation=90)

    # Add text labels to each bar in the plot
    for index, row in total_emissions.iterrows():
        plt.text(index, row[gas], f'{row[gas]:.2f}', color='black', ha="center")

    plt.show()

########################################################## MENU OPTION 5 ##########################################################

def find_top_polluting_sources(file_path):
    """
    Helps in figuring out top 4 most polluting entities for each GHG, from a sub-sector of a specific sector.

    Parameters:
    - file_path: Path to the emissions data CSV file.

    Prints:
    - Top 4 most polluting sources for each greenhouse gas.
    """

    try:
        # Load the CSV file into a DataFrame
        df = pd.read_csv(file_path)

        # Check if 'start_time' column exists and convert to datetime to extract the year
        if 'start_time' in df.columns:
            df['start_time'] = pd.to_datetime(df['start_time'])
            df['year'] = df['start_time'].dt.year

        # Convert infinite values to NaN for better handling of data
        df.replace([np.inf, -np.inf], np.nan, inplace=True)

        # Clean the data by filling NaN values
        for col in df.columns:
            if df[col].dtype == 'object':
                df[col].fillna('NA', inplace=True)
            else:
                df[col].fillna(0, inplace=True)

        # Map subsectors to their respective sectors using a predefined dictionary
        sectors_mapping = {
            'agriculture': ['cropland-fires', 'enteric-fermentation-cattle-feedlot', 'enteric-fermentation-cattle-pasture', 'enteric-fermentation-other', 'manure-left-on-pasture-cattle', 'manure-management-cattle-feedlot', 'manure-management-other', 'other-agricultural-soil-emissions', 'rice-cultivation', 'synthetic-fertilizer-application'],
            'buildings': ['residential-and-commercial-onsite-fuel-usage', 'other-onsite-fuel-usage'],
            'fluorinatedGases': ['fluorinated-gases'],
            'fossilFuelOperations': ['coal-mining', 'oil-and-gas-production-and-transport', 'oil-and-gas-refining', 'other-fossil-fuel-operations', 'solid-fuel-transformation'],
            'forestryAndLandUse': ['shrubgrass-fires', 'removals', 'forest-land-fires', 'wetland-fires', 'forest-land-degradation', 'net-shrubgrass', 'forest-land-clearing', 'net-forest-land', 'net-wetland', 'water-reservoirs'],
            'manufacturing': ['aluminum', 'steel', 'cement', 'petrochemicals', 'chemicals', 'other-manufacturing', 'pulp-and-paper'],
            'mineralExtraction': ['bauxite-mining', 'copper-mining', 'iron-mining', 'rock-quarrying', 'sand-quarrying'],
            'power': ['electricity-generation', 'other-energy-use'],
            'transportation': ['domestic-aviation', 'domestic-shipping', 'international-aviation', 'international-shipping', 'other-transport', 'railways', 'road-transportation'],
            'waste': ['biological-treatment-of-solid-waste-and-biogenic', 'incineration-and-open-burning-of-waste', 'solid-waste-disposal', 'wastewater-treatment-and-discharge']
        }

        # Function to find the top 4 most polluting unique source IDs for a given gas, excluding certain source names
        def top_polluting_sources(gas, exclude_sources=[]):
            # Filter data for the specific gas
            gas_data = df[df['gas'] == gas] if 'gas' in df.columns else pd.DataFrame()
            
            if gas_data.empty:
                return gas_data
            
            # Exclude specified source names
            if 'source_name' in gas_data.columns:
                for source_name in exclude_sources:
                    gas_data = gas_data[gas_data['source_name'] != source_name]

            # Sort data by emissions_quantity in descending order
            if 'emissions_quantity' in gas_data.columns:
                gas_data = gas_data.sort_values(by='emissions_quantity', ascending=False)
            
            # Drop duplicates based on source_id to keep only unique source IDs
            if 'source_id' in gas_data.columns:
                gas_data = gas_data.drop_duplicates(subset='source_id')

            # Take the top 4 rows
            top_polluting = gas_data.head(4)
            
            # Extract relevant information, check if columns exist
            columns = ['source_id', 'source_name', 'source_type', 'subsector', 'year', 'gas', 'emissions_quantity', 'geometry_ref']
            results = top_polluting[[col for col in columns if col in top_polluting.columns]]
            
            return results

        # List of greenhouse gases to consider
        greenhouse_gases = df['gas'].unique() if 'gas' in df.columns else []

        # Print the name of the input file
        print(f"\nInput file: {file_path}\n")

        # Find the top 4 most polluting sources for each gas (excluding 'India' as source_name)
        results = pd.DataFrame()
        for gas in greenhouse_gases:
            top_sources = top_polluting_sources(gas, exclude_sources=['India'])
            results = pd.concat([results, top_sources])

        # Display the results
        print("Top 4 most polluting sources for each greenhouse gas:")
        print(results)
        print("")

    except FileNotFoundError:
        print(f"Error: The file at path '{file_path}' was not found.")
    except ValueError as ve:
        print(f"Error: {ve}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

########################################################## MAIN ##########################################################

# Function to display a menu and handle user inputs
def menu():
    """
    Display the main menu and handle user inputs.
    """
    while True:
        print("\nMenu:")
        print("1. Check if a point is within a specified grid.")
        print("2. Calculate emissions profiles for aggregated grid cells.")
        print("3. Plot total emissions by sector and gas for a specified year.")
        print("4. Plot total emissions by subsector for a specified gas.")
        print("5. Find top 4 most polluting entities for each GHG from a sub-sector")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ")  # Prompt user for choice

        if choice == '1':  # Option 1: Check if a point is within a specified grid
            center_lat = float(input("\nEnter the center latitude of the grid: "))  # Input center latitude
            center_lon = float(input("Enter the center longitude of the grid: "))  # Input center longitude
            point_lat = float(input("Enter the latitude of the point: "))  # Input point latitude
            point_lon = float(input("Enter the longitude of the point: "))  # Input point longitude
            grid_size_km = float(input("Enter the grid size in km: "))  # Input grid size in kilometers
            is_within_grid_corrected(center_lat, center_lon, point_lat, point_lon, grid_size_km)  # Function call
        elif choice == '2':  # Option 2: Calculate emissions profiles for aggregated grid cells
            file_path = input("\nEnter the path to the emissions CSV file: ")  # Input file path
            calculate_emissions_profiles(file_path)  # Function call
        elif choice == '3':  # Option 3: Plot total emissions by sector and gas for a specified year
            plot_total_emissions_by_sector_and_gas()  # Function call
        elif choice == '4':  # Option 4: Plot total emissions by subsector for a specified gas
            file_path = input("\nEnter the path to the emissions CSV file: ")  # Input file path
            gas = input("Enter the greenhouse gas (e.g., co2, ch4, n2o, co2e_100yr, co2e_20yr): ")  # Input greenhouse gas
            plot_total_emissions_by_subsector(file_path, gas)  # Function call
        elif choice == '5':
            file_path = input("\nEnter the path to the emissions data CSV file: ").strip()
            find_top_polluting_sources(file_path) 
            break
        elif choice == '6':  # Option 5: Exit the application
            print("\nExiting the application. Thank you!\n")
            break  # Exit the loop and terminate the program
        else:  # Invalid input
            print("\nInvalid choice. Please enter a number between 1 and 6.")  # Error message

# Entry point of the program
if __name__ == "__main__":
    menu()  # Call the menu function to start the application
