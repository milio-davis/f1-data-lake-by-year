import boto3
import pandas as pd
import io
import requests
import os

# Input desired year of information
year_data = 2025

bucket = os.environ.get('S3_BUCKET')

ergast_base_url = "https://api.jolpi.ca/ergast/f1/"
# Docs: https://github.com/jolpica/jolpica-f1/blob/main/docs/README.md

def get_drivers_df(year):
    """ Retrieves Formula 1 driver data for a given year from the Ergast API.
    Parameters: year (int or str): The season year to fetch data for.
    Returns: pandas.DataFrame: A DataFrame with driver details. """
    
    url = f"{ergast_base_url}/{year}/drivers/"
    response = requests.get(url)
    
    drivers_list = response.json()['MRData']['DriverTable']['Drivers']
    drivers_df = pd.json_normalize(drivers_list)
    
    drivers_df['season'] = year_data
    
    # Rename columns
    drivers_df = drivers_df.rename(columns={'driverId': 'driver_id', 'permanentNumber': 'permanent_number', 'givenName': 'given_name'
        , 'familyName': 'family_name', 'dateOfBirth': 'birth_day'})
    
    # Assign types
    drivers_df = drivers_df.astype({'permanent_number': int, 'birth_day': 'datetime64[ns]'})
    
    return drivers_df

def get_constructors_df(year):
    """ Retrieves Formula 1 constructor data for a given year from the Ergast API.
    Parameters: year (int or str): The season year to fetch data for.
    Returns: pandas.DataFrame: A DataFrame with constructor details. """
    
    url = f"{ergast_base_url}/{year}/constructors/"
    response = requests.get(url)
    
    constructors_list = response.json()['MRData']['ConstructorTable']['Constructors']
    constructors_df = pd.json_normalize(constructors_list)
    
    constructors_df['season'] = year_data
    
    # Rename columns
    constructors_df = constructors_df.rename(columns={'constructorId': 'constructor_id'})
    
    return constructors_df

def get_races_calendar_df(year):
    """ Retrieves Formula 1 calendar races data for a given year from the Ergast API.
    Parameters: year (int or str): The season year to fetch data for.
    Returns: pandas.DataFrame: A DataFrame with calendar races details. """
    
    url = f"{ergast_base_url}/{year}"
    response = requests.get(url)
    
    races_list = response.json()['MRData']['RaceTable']['Races']    
    races_df = pd.json_normalize(races_list)

    races_df['season'] = year_data
    
    # Drop unnecessary columns
    races_df.drop(['FirstPractice.time', 'SecondPractice.time', 'ThirdPractice.time', 'SprintQualifying.date'
        , 'SprintQualifying.time', 'Sprint.time', 'Qualifying.time'], axis=1, inplace=True, errors='ignore')
    
    # Rename columns
    races_df = races_df.rename(columns={'raceName': 'race_name', 'url': 'url_grand_prix'
        , 'Circuit.circuitId': 'circuit_id', 'Circuit.url': 'url_circuit'
        , 'Circuit.circuitName': 'name', 'Circuit.Location.lat': 'location_lat', 'Circuit.Location.long': 'location_long'
        , 'Circuit.Location.locality': 'location_locality', 'Circuit.Location.country': 'country'
        , 'FirstPractice.date': 'practice1_date', 'SecondPractice.date': 'practice2_date', 'ThirdPractice.date': 'practice3_date'
        , 'Qualifying.date': 'qualifying_date', 'Sprint.date': 'sprint_date'})
    
    # Assign types
    races_df = races_df.astype({'season': int, 'round': int, 'date': 'datetime64[ns]', 'location_lat': float, 'location_long': float
        , 'practice1_date': 'datetime64[ns]', 'practice2_date': 'datetime64[ns]', 'practice3_date': 'datetime64[ms]'
        , 'qualifying_date': 'datetime64[ns]', 'sprint_date': 'datetime64[ns]'})
    
    return races_df

def get_races_results_df(year, year_races_calendar_df):
    """ Retrieves Formula 1 calendar races data for a given year from the Ergast API.
    Parameters: year (int or str): The season year to fetch data for.
    Returns: pandas.DataFrame: A DataFrame with calendar races details. """
    
    # Start season races pd df
    races_df = pd.DataFrame()

    # Get season length
    season_length = len(year_races_calendar_df.index)

    # For each race
    for round_index in range(1,season_length+1):
        try:
            url = f"{ergast_base_url}/{year}/{round_index}/results"
            response = requests.get(url)
            
            # Get race result into a pd df
            race_result_df = pd.json_normalize(response.json()['MRData']['RaceTable']['Races'][0]['Results'])
            
            # Add circuit id, season year, round id
            race_row = year_races_calendar_df.loc[year_races_calendar_df['round'].astype(int) == round_index]

            race_result_df['raceRoundId'] = race_row['round'].values[0]
            race_result_df['seasonYear'], race_result_df['circuitId'] = race_row['season'].values[0], race_row['circuit_id'].values[0]
            
            # Add race result df to season races df
            races_df = pd.concat([races_df, race_result_df], ignore_index=True)
        except:
            # If no more races
            break 
    
    # Keep these columns 
    races_df = races_df[['number','position','positionText','points','grid','laps','status','Driver.permanentNumber','Driver.code'
        ,'Constructor.constructorId','Time.millis','Time.time','FastestLap.rank','FastestLap.lap','FastestLap.Time.time'
        ,'raceRoundId','seasonYear','circuitId']]
    
    # Rename columns
    races_df = races_df.rename(columns={'number': 'driver_number', 'positionText': 'position_text'
        , 'Driver.permanentNumber': 'driver_permanent_number', 'Driver.code': 'driver_code'
        , 'Constructor.constructorId': 'constructor_id', 'Time.millis': 'time_millis', 'Time.time': 'time_interval'
        , 'FastestLap.rank': 'fastest_lap_rank', 'FastestLap.lap': 'fastest_lap_lap', 'FastestLap.Time.time': 'fastest_lap_time'
        , 'raceRoundId': 'race_round_id', 'seasonYear': 'season', 'circuitId': 'race_circuit_id'})
    
    # Fill NaN
    races_df.fillna({'fastest_lap_rank': 0, 'fastest_lap_lap': 0, 'season': 0, 'race_round_id': 0}, inplace=True)
    
    # Assign types
    races_df = races_df.astype({'driver_number': int, 'position': int, 'points': float, 'grid': int, 'laps': int
        , 'driver_permanent_number': int, 'time_millis': float, 'fastest_lap_rank': int, 'fastest_lap_lap': int
        , 'race_round_id': int, 'season': int})
    
    return races_df

def upload_df_to_s3(bucket, key, df):
    """Uploads a pandas DataFrame as a CSV file to an S3 bucket.
    Parameters: bucket (str): Name of the target S3 bucket.
        key (str): S3 object key (path/filename).
        df (pandas.DataFrame): DataFrame to upload. """

    s3 = boto3.client('s3')
    parquet_buffer = io.BytesIO()
    # Write the DataFrame as a Parquet file in memory
    df.to_parquet(parquet_buffer, index=False, engine='pyarrow')
    # Upload to S3
    s3.put_object(Bucket=bucket, Key=key, Body=parquet_buffer.getvalue())

def lambda_handler(event, context):
    # Get data to dataframes
    print("Fetching drivers, constructors, calendar and race results info...")
    year_drivers_df = get_drivers_df(year_data)
    year_constructors_df = get_constructors_df(year_data)
    year_races_calendar_df = get_races_calendar_df(year_data)
    year_results_df = get_races_results_df(year_data, year_races_calendar_df)

    # Upload to S3
    print("Uploading drivers, constructors, calendar and race results csv to S3...")
    upload_df_to_s3(bucket, f"raw/drivers/year={year_data}/drivers.parquet", year_drivers_df)
    upload_df_to_s3(bucket, f"raw/constructors/year={year_data}/constructors.parquet", year_constructors_df)
    upload_df_to_s3(bucket, f"raw/races/year={year_data}/races.parquet", year_races_calendar_df)
    upload_df_to_s3(bucket, f"raw/results/year={year_data}/results.parquet", year_results_df)

    return {
        "statusCode": 200,
        "body": "Uploaded all F1 tables to S3 successfully."
    }
