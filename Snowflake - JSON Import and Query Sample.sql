--Loading heart rate data from FitBit to Snowflake
	--Importing from local file system: https://support.snowflake.net/s/article/importing-data-from-a-local-file
		--See file:// format below for Windows machines
	--Querying JSON files: https://docs.snowflake.com/en/user-guide/json-basics-tutorial-query.html

--Move to the FitBit database
USE DATABASE FitBit;

--Create the file format for json load in FitBit database
create or replace file format myjsonformat
							  type='JSON'
							  strip_outer_array=true;

--Create a table to hold raw json
create or replace table heart_rate	(
									src variant
									)
						Stage_file_format = myjsonformat;


--PUT the file into the stage table
PUT file://C:\Users\benni\Downloads\BennieRegenold\user-site-export\heart_rate-20*.json @%heart_rate;

--COPY data into the table
COPY INTO HEART_RATE;

--Create a flattened table
CREATE or replace table heart_rate_flat as
										SELECT
										to_timestamp(measurement_timestamp, 'MM/DD/YY HH24:MI:SS') as measurement_dt,
										bpm,
										confidence
										FROM(
											 select
												src:dateTime::string as measurement_timestamp
												,value:bpm::int as bpm
												,value:confidence::int as confidence
												from HEART_RATE
												,lateral flatten( input => src)
												where
												value:bpm is not null
											);