import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, box
import math
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from decimal import Decimal
from pandas.api.types import CategoricalDtype
#import csv

########################################################## MENU OPTION 1 ##########################################################

def is_within_grid_corrected(center_lat, center_lon, point_lat, point_lon, grid_size_km):
    """
    Check if a point (point_lat, point_lon) is within a grid centered at (center_lat, center_lon) with a specified size.
    
    Parameters:
    - center_lat, center_lon: Latitude and longitude of the center of the grid.
    - point_lat, point_lon: Latitude and longitude of the point to check.
    - grid_size_km: Size of the grid in kilometers.
    
    Returns:
    - True if the point is within the grid, False otherwise.
    """
    # Constants
    km_per_deg_lat = 111.0  # Approximate conversion factor for latitude to kilometers
    
    # Calculate degree per km at the given latitude for longitude
    km_per_deg_lon = 111.0 * math.cos(math.radians(center_lat))
    
    # Calculate the bounding box (half the grid size in each direction)
    lat_min = center_lat - (grid_size_km / (2 * km_per_deg_lat))
    lat_max = center_lat + (grid_size_km / (2 * km_per_deg_lat))
    lon_min = center_lon - (grid_size_km / (2 * km_per_deg_lon))
    lon_max = center_lon + (grid_size_km / (2 * km_per_deg_lon))
    
    # Check if the point is within the bounding box
    within_grid = lat_min <= point_lat <= lat_max and lon_min <= point_lon <= lon_max
    
    # Print result
    if within_grid:
        print(f"\nThe point ({point_lat}, {point_lon}) is within the {grid_size_km} km grid centered at ({center_lat}, {center_lon}).\n")
    else:
        print(f"\nThe point ({point_lat}, {point_lon}) is NOT within the {grid_size_km} km grid centered at ({center_lat}, {center_lon}).\n")
    
    # Print the bounding box values
    print(f"Bounding box for the {grid_size_km} km grid centered at ({center_lat}, {center_lon}):")
    print(f"Latitude range: {lat_min} to {lat_max}")
    print(f"Longitude range: {lon_min} to {lon_max}")
    
    return within_grid

########################################################## MENU OPTION 2 ##########################################################

def calculate_emissions_profiles():
    """
    Calculate emissions profiles for aggregated grid cells over multiple years, specified by the user.
    """
    # Load the CSV file into a DataFrame
    file_path = 'IND/DATA/agriculture/cropland-fires_emissions_sources.csv'
    df = pd.read_csv(file_path)

    # Check if 'start_time' and 'end_time' columns exist, and extract year information
    if 'start_time' in df.columns and 'end_time' in df.columns:
        df['year'] = pd.to_datetime(df['start_time']).dt.year
    else:
        df['year'] = df['year']

    # Ensure 'longitude' and 'latitude' columns are present and create a GeoDataFrame
    geometry = [Point(xy) for xy in zip(df.lon, df.lat)]
    gdf = gpd.GeoDataFrame(df, geometry=geometry)

    # Prompt user for grid cell coordinates
    cell_x_min = float(input("Enter the minimum longitude of the starting grid cell: "))
    cell_y_min = float(input("Enter the minimum latitude of the starting grid cell: "))

    # Prompt user for the area size in km
    cell_size_km = float(input("Enter the grid cell size in km: "))
    km_per_deg_lat = 111.0  # Approximate conversion factor for latitude to kilometers
    km_per_deg_lon = 111.0 * math.cos(math.radians(cell_y_min))  # Adjust based on latitude

    cell_size_deg_lat = cell_size_km / km_per_deg_lat
    cell_size_deg_lon = cell_size_km / km_per_deg_lon

    # Calculate the maximum latitude and longitude for the grid
    max_lat = cell_y_min + cell_size_deg_lat
    max_lon = cell_x_min + cell_size_deg_lon

    # Create the initial grid cell as a GeoDataFrame
    initial_cell = box(cell_x_min, cell_y_min, max_lon, max_lat)
    initial_cell_gdf = gpd.GeoDataFrame([initial_cell], columns=['geometry'])

    # Prompt user for the list of years of interest
    years_of_interest_str = input("Enter the list of years of interest (comma-separated): ")
    years_of_interest = [int(year.strip()) for year in years_of_interest_str.split(',')]

    # Initialize a dictionary to store emissions profiles for each year
    emissions_profiles = {year: {} for year in years_of_interest}

    # Process each year of interest
    for year in years_of_interest:
        yearly_data = gdf[gdf['year'] == year]
        
        # Perform spatial join to find emissions sources within the current grid cell
        joined_cell = gpd.sjoin(yearly_data, initial_cell_gdf, how='inner', predicate='within')
        
        if not joined_cell.empty:
            # Aggregate emissions for the current grid cell by gas type
            cell_emissions = joined_cell.groupby('gas')['emissions_quantity'].sum()
            
            # Store emissions profile for the current grid cell
            emissions_profiles[year][f'Cell: {cell_x_min}, {cell_y_min}'] = cell_emissions

    # Output the emissions profiles for each grid cell for each year
    for year, profiles in emissions_profiles.items():
        print(f"\nEmissions Profiles for {year}:")
        for cell, profile in profiles.items():
            print(f"\n{cell}:")
            for gas, quantity in profile.items():
                print(f"{gas}: {quantity} Metric Tonnes")

    # Leave a blank line
    print("")

########################################################## MENU OPTION 3 ##########################################################

def plot_total_emissions_by_sector_and_gas():
    """
    Plot total greenhouse gas emissions by sector for a specified year and gas.
    """
    file_path = input("Enter the path to the emissions CSV file: ")

    try:
        # Load the CSV file into a DataFrame
        df = pd.read_csv(file_path)

        # Convert infinite values to NaN for better handling of data
        df.replace([np.inf, -np.inf], np.nan, inplace=True)

        # Clean the data by filling NaN values
        for col in df.columns:
            if df[col].dtype == 'object':
                df[col].fillna('NA', inplace=True)
            else:
                df[col].fillna(0, inplace=True)

        # Convert appropriate columns to numeric, handling errors by coercing problematic entries to NaN
        df['co2'] = pd.to_numeric(df['co2'], errors='coerce')
        df['ch4'] = pd.to_numeric(df['ch4'], errors='coerce')
        df['n2o'] = pd.to_numeric(df['n2o'], errors='coerce')
        df['co2e_100yr'] = pd.to_numeric(df['co2e_100yr'], errors='coerce')
        df['co2e_20yr'] = pd.to_numeric(df['co2e_20yr'], errors='coerce')

        # Define the sectors mapping dictionary
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

        # Function to map each subsector to its corresponding sector
        def get_sector(subsector):
            for sector, subsectors in sectors_mapping.items():
                if subsector in subsectors:
                    return sector
            return 'Unknown'

        # Apply the function to create a new 'sector' column in the DataFrame
        df['sector'] = df['sub_sector'].apply(get_sector)

        # User input for the year
        year = int(input("Enter the year for which you want the greenhouse gas distributions (e.g., 2020): "))

        def plot_total_emissions_by_sector(df, gas, year):
            # Filter the DataFrame for the specified year
            df_year = df[df['year'] == year]

            # Sum emissions by sector for the specified gas
            total_emissions = df_year.groupby('sector')[gas].sum().reset_index()
            plt.figure(figsize=(14, 8))
            sns.barplot(data=total_emissions, x='sector', y=gas, palette='tab20')
            plt.title(f'Total {gas} Emissions by Sector in {year}')
            plt.xlabel('Sector')
            plt.ylabel(f'Total {gas} Emissions')
            plt.xticks(rotation=45)

            # Annotate each bar with its value
            for index, row in total_emissions.iterrows():
                plt.text(index, row[gas], f'{row[gas]:.2f}', color='black', ha="center")

            plt.show()

        # Plot total emissions by sector for each specified gas for the given year
        for gas in ['co2', 'ch4', 'n2o', 'co2e_100yr', 'co2e_20yr']:
            plot_total_emissions_by_sector(df, gas, year)

    except FileNotFoundError:
        print(f"Error: The file at path '{file_path}' was not found.")
    except ValueError as ve:
        print(f"Error: {ve}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

########################################################## MENU OPTION 4 ##########################################################

def plot_total_emissions_by_subsector(file_path, gas):
    """
    Plot total emissions by subsector for a specified gas.

    Parameters:
    - file_path: Path to the emissions data CSV file.
    - gas: Type of gas emissions ('co2', 'ch4', 'n2o', 'co2e_100yr', 'co2e_20yr').
    """
    # Load the CSV file into a DataFrame
    df = pd.read_csv(file_path)

    # Convert infinite values to NaN for better handling of data
    df.replace([np.inf, -np.inf], np.nan, inplace=True)

    # Clean the data by filling NaN values
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col].fillna('NA', inplace=True)
        else:
            df[col].fillna(0, inplace=True)

    # Convert appropriate columns to numeric, handling errors by coercing problematic entries to NaN
    df['co2'] = pd.to_numeric(df['co2'], errors='coerce')
    df['ch4'] = pd.to_numeric(df['ch4'], errors='coerce')
    df['n2o'] = pd.to_numeric(df['n2o'], errors='coerce')
    df['co2e_100yr'] = pd.to_numeric(df['co2e_100yr'], errors='coerce')
    df['co2e_20yr'] = pd.to_numeric(df['co2e_20yr'], errors='coerce')

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

    # Define a function to map each subsector to its corresponding sector
    def get_sector(subsector):
        for sector, subsectors in sectors_mapping.items():
            if subsector in subsectors:
                return sector
        return 'Unknown'

    # Apply the function to create a new 'sector' column in the DataFrame
    df['sector'] = df['sub_sector'].apply(get_sector)

    def plot_total_emissions(df, gas):
        total_emissions = df.groupby(['sector', 'sub_sector'])[gas].sum().reset_index()
        unique_sectors = total_emissions['sector'].unique()

        for sector in unique_sectors:
            sector_data = total_emissions[total_emissions['sector'] == sector]
            plt.figure(figsize=(14, 8))
            sns.barplot(data=sector_data, x=gas, y='sub_sector', palette='tab20', orient='h')
            plt.title(f'Total {gas} Emissions by Subsector for {sector.capitalize()} Sector')
            plt.xlabel(f'Total {gas} Emissions')
            plt.ylabel('Subsector')
            plt.xticks(rotation=90)

            # Annotate each bar with its value
            for index, row in sector_data.iterrows():
                plt.text(row[gas], index, f'{row[gas]:.2f}', color='black', va="center")

            plt.tight_layout()
            plt.show()

    # Plot total emissions by subsector for the specified gas
    plot_total_emissions(df, gas)


def sub_sectoral_data_insights_menu():
    """
    Sub-Sectoral Data Insights menu-driven application.
    """
    print("Welcome to Sub-Sectoral Data Insights!")

    # Prompt user for file path
    file_path = input("Enter the path to the emissions data CSV file: ").strip()

    while True:
        print("\nPlease select from the following options:")
        print("1. Plot total CO2 emissions by subsector")
        print("2. Plot total CH4 emissions by subsector")
        print("3. Plot total N2O emissions by subsector")
        print("4. Plot total CO2e (100-year) emissions by subsector")
        print("5. Plot total CO2e (20-year) emissions by subsector")
        print("6. Exit")

        choice = input("\nEnter your choice (1-6): ")

        if choice == '1':
            plot_total_emissions_by_subsector(file_path, 'co2')
        elif choice == '2':
            plot_total_emissions_by_subsector(file_path, 'ch4')
        elif choice == '3':
            plot_total_emissions_by_subsector(file_path, 'n2o')
        elif choice == '4':
            plot_total_emissions_by_subsector(file_path, 'co2e_100yr')
        elif choice == '5':
            plot_total_emissions_by_subsector(file_path, 'co2e_20yr')
        elif choice == '6':
            print("Exiting the application. Thank you!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 6.")

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


def main():
    """
    Main function to run the emissions data analysis application.
    """
    print("Welcome to the GHG Emissions Data Analysis Application!")

    while True:
        print("\nPlease select from the following options:")
        print("1. Check if a point is within a specified grid")
        print("2. Calculate emissions profile for a specified grid cell")
        print("3. Plot Total Emissions by Sector and Gas")
        print("4. Find total greenhouse gas emissions by sub-sector for a specified year")
        print("5. Find top 4 most polluting entities for each GHG from a sub-sector")
        print("6. Exit")

        choice = input("\nEnter your choice (1-6): ")

        if choice == '1':
            center_lat = float(input("Enter the latitude of the center of the grid: "))
            center_lon = float(input("Enter the longitude of the center of the grid: "))
            point_lat = float(input("Enter the latitude of the point to check: "))
            point_lon = float(input("Enter the longitude of the point to check: "))
            grid_size_km = float(input("Enter the size of the grid in kilometers: "))
            
            is_within_grid_corrected(center_lat, center_lon, point_lat, point_lon, grid_size_km)

        elif choice == '2':
            calculate_emissions_profiles()

        elif choice == '3':
            plot_total_emissions_by_sector_and_gas()

        elif choice == '4':
            sub_sectoral_data_insights_menu()

        elif choice == '5':
            file_path = input("Enter the path to the emissions data CSV file: ").strip()
            find_top_polluting_sources(file_path) 

        elif choice == '6':
            print("\nExiting the application. Thank you!\n")
            break
        # Ask user if they want to continue or exit
        if not continue_or_exit():
            break

        else:
            print("Invalid choice. Please enter a number from 1 to 6.")

def continue_or_exit():
    """
    Asks the user if they want to continue with another option or exit the program.

    Returns:
    - True if user wants to continue, False if user wants to exit.
    """
    while True:
        choice = input("\n\nDo you want to try another option? (yes/no): ").strip().lower()
        if choice in ['yes', 'y']:
            return True
        elif choice in ['no', 'n']:
            return False
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

# Run the main function to start the application
if __name__ == "__main__":
    main()
