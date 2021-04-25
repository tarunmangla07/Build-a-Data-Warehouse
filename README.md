# Introduction
The user base of a music streaming startup called as ``sparkify`` has grown tremendously and due to which they want their processes and data on to cloud.
The entire data resides in Amazon S3  in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

The company wants to build an ETL pipeline that extracts the S3 data and stages in Redshift and then transforms the data into a set of tables to easily get insights about the songs their users are listening to.

# Star Schema
In the star schema, we have a ``Fact Table `` called as ``songplays`` and various ``dimension Tables`` such as ``users``, ``songs``, ``àrtists`` and ``time``

## Staging Tables
* staging_events - staging table to store log data 
    * Columns - artist, auth, firstName, gender, itemInSession, lastName, length, level, location, method, page, registration, sessionId, song, status, ts, userAgent, userId.

* staging_songs - staging table to store song data
    * Columns -  num_songs, artist_id, artist_latitude, artist_longitude, artist_location, artist_name, song_id, title, duration, year.

## Fact Table
* songplays -  records in log data associated with song plays
    * Columns - songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent

## Dimension Table
* users - users in the app
    * Columns - user_id, first_name, last_name, gender, level
* songs - songs in music database
    * Columns - song_id, title, artist_id, year, duration
* artists - artists in music database
    * Columns - artist_id, name, location, latitude, longitude
* time - timestamp of records in songplays broken down into specific units
    * Columns - start_time, hour, day, week, month, year, weekday
   
# ETL pipeline 

The ETL pipeline consists loads the data stored in S3 to Redshift staging event and staging song tables and then insert the data to the above Facts and dimension tables from the staging event and staging song tables.

# How to get Started
Please follow the below steps in order to get the project running:
* Make sure the project consists of the following files:
    * ``create_tables.py`` - Script to initiate the database connection and create and drop tables.
    * ``dwh.cfg`` - configuration file containing all the aws related information.
    * ``Redshift_Cluster_Launch.ipynb`` - Jupyter notebook to launch the Redshift Cluster on AWS.
    * ```sql_queries.py``` - It contains create, copy and insert statements for the database
    * ``Test.ipynb`` - Jupyter notebook to check if data has been inserted in the final tables.
* when all the files are in place, now we are ready to run the project as:
    * First insert AWS key and secret access key and other parameters relevant to launch a redshift cluster in ``dwh.cfg``
    * Now run ``Redshift_Cluster_Launch.ipynb`` in order to launch a redshift Cluster on aws.
    * Run ``create_tables.py`` script in order to drop and create the staging, fact and dimension tables.
    * Run ``etl.py`` script to load the data from S3 to staging tables and then insert data into fact and dimension tables.
    * Run ``Test.ipynb`` to check whether the data is inserted in Fact and dimension tables.
    * Finally Run the delete blocks of ``Redshift_Cluster_Launch.ipynb`` in order to delete the cluster and detach the policies.