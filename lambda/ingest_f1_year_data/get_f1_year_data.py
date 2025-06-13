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
    return pd.json_normalize(drivers_list)

def get_constructors_df(year):
    """ Retrieves Formula 1 constructor data for a given year from the Ergast API.
    Parameters: year (int or str): The season year to fetch data for.
    Returns: pandas.DataFrame: A DataFrame with constructor details. """
    
    url = f"{ergast_base_url}/{year}/constructors/"
    response = requests.get(url)
    constructors_list = response.json()['MRData']['ConstructorTable']['Constructors']
    return pd.json_normalize(constructors_list)

def get_calendar_df(year):
    """ Retrieves Formula 1 calendar races data for a given year from the Ergast API.
    Parameters: year (int or str): The season year to fetch data for.
    Returns: pandas.DataFrame: A DataFrame with calendar races details. """
    
    url = f"{ergast_base_url}/{year}"
    response = requests.get(url)
    races_list = response.json()['MRData']['RaceTable']['Races']
    return pd.json_normalize(races_list)

def get_races_results_df(year, year_races_calendar_df):
    """ Retrieves Formula 1 calendar races data for a given year from the Ergast API.
    Parameters: year (int or str): The season year to fetch data for.
    Returns: pandas.DataFrame: A DataFrame with calendar races details. """
    
    races_df = pd.DataFrame()
    season_length = len(year_races_calendar_df.index)

    for round_index in range(1,season_length+1):
        url = f"{ergast_base_url}/{year}/{round_index}/results"
        response = requests.get(url)
        try:
            race_result_df = pd.json_normalize(response.json()['MRData']['RaceTable']['Races'][0]['Results'])
            races_df = pd.concat([races_df, race_result_df], ignore_index=True)
        except:
            break
    
    races_df = races_df[['number','position','positionText','points','grid','laps','status'
        ,'position','Driver.permanentNumber','Driver.code'
        ,'Constructor.constructorId','Time.millis','Time.time','FastestLap.rank','FastestLap.lap','FastestLap.Time.time']]
    
    return races_df

def upload_df_to_s3(bucket, key, df):
    """Uploads a pandas DataFrame as a CSV file to an S3 bucket.
    Parameters: bucket (str): Name of the target S3 bucket.
        key (str): S3 object key (path/filename).
        df (pandas.DataFrame): DataFrame to upload. """

    s3 = boto3.client('s3')
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    s3.put_object(Bucket=bucket, Key=key, Body=csv_buffer.getvalue())

def lambda_handler(event, context):
    # Get data to dataframes
    print("Fetching drivers, calendar and race results info...")
    year_drivers_df = get_drivers_df(year_data)
    year_constructors_df = get_constructors_df(year_data)
    year_races_calendar_df = get_calendar_df(year_data)
    #year_results_df = get_races_results_df(year_data, year_races_calendar_df)

    # Upload to S3
    print("Uploading drivers, calendar and race results csv to S3...")
    upload_df_to_s3(bucket, f"raw/{year_data}/drivers.csv", year_drivers_df)
    upload_df_to_s3(bucket, f"raw/{year_data}/constructors.csv", year_constructors_df)
    upload_df_to_s3(bucket, f"raw/{year_data}/races.csv", year_races_calendar_df)
    #upload_df_to_s3(bucket, f"raw/{year_data}/results.csv", year_results_df)

    return {
        "statusCode": 200,
        "body": "Uploaded all F1 tables to S3 successfully."
    }