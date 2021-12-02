import urllib.request
import os

def create_irradiance_file(lat, lon, year):

    # Declare all variables as strings. Spaces must be replaced with '+', i.e., change 'John Smith' to 'John+Smith'.
    # Define the lat, long of the location and the year
    #lat, lon, year = 47.65,-122.3,2019
    # You must request an NSRDB api key from the link above
    api_key = 'dYmj0MPsG0ngTV1VdHqmTUEe4TPX9fxIS45FsOal'
    # Set the attributes to extract (e.g., dhi, ghi, etc.), separated by commas.
    attributes = 'ghi,dhi,dni,wind_speed,air_temperature,solar_zenith_angle'
    # Choose year of data
    #year = '2019'
    # Set leap year to true or false. True will return leap day data if present, false will not.
    leap_year = 'false'
    # Set time interval in minutes, i.e., '30' is half hour intervals. Valid intervals are 30 & 60.
    interval = '60'
    # Specify Coordinated Universal Time (UTC), 'true' will use UTC, 'false' will use the local time zone of the data.
    # NOTE: In order to use the NSRDB data in SAM, you must specify UTC as 'false'. SAM requires the data to be in the
    # local time zone.
    utc = 'false'
    # Your full name, use '+' instead of spaces.
    your_name = 'Cassidy+Quigley'
    # Your reason for using the NSRDB.
    reason_for_use = 'beta+testing'
    # Your affiliation
    your_affiliation = 'University+of+Washington'
    # Your email address
    your_email = 'ccq@uw.edu'
    # Please join our mailing list so we can keep you up-to-date on new developments.
    mailing_list = 'false'

    print('lat', lat)
    print('lon', lon)
    print('year', year)

    # Declare url string
    url = 'https://developer.nrel.gov/api/solar/nsrdb_psm3_download.csv?wkt=POINT({lon}%20{lat})&names={year}&leap_day={leap}&interval={interval}&utc={utc}&full_name={name}&email={email}&affiliation={affiliation}&mailing_list={mailing_list}&reason={reason}&api_key={api}&attributes={attr}'.format(year=year, lat=lat, lon=lon, leap=leap_year, interval=interval, utc=utc, name=your_name, email=your_email, mailing_list=mailing_list, affiliation=your_affiliation, reason=reason_for_use, api=api_key, attr=attributes)
    
    data_path = os.path.abspath('../data')
    
    test = urllib.request.urlretrieve(url, data_path + '/irradiance.csv')
