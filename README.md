# Background
I have decided to hypothetically treat myself to a long holiday vacation in Honolulu, Hawaii. To help with my trip planning, I decided to do a climate analysis about the area. The following sections outline the steps that i took to accomplish this task.

## Part 1: Analyze and Explore the Climate Data
In this section, I used Python and SQLAlchemy to do a basic climate analysis and data exploration of the climate database. Specifically, I used SQLAlchemy ORM queries, Pandas, and Matplotlib. To do so, I completed the following steps:

1. Used the SQLAlchemy create_engine() function to connect to my SQLite database.

2. Used the SQLAlchemy automap_base() function to reflect the tables into classes, and then saved references to the classes named station and measurement.

3. Linked Python to the database by creating a SQLAlchemy session.

4. Performed a precipitation analysis and then a station analysis by completing the steps in the following two subsections.

### Precipitation Analysis

1. Found the most recent date in the dataset.

2. Used that date, got the previous 12 months of precipitation data by querying the previous 12 months of data.

3. Loaded the query results into a Pandas DataFrame. Explicitly set the column names.

4. Sorted the DataFrame values by "date".

5. Plotted the results by using the DataFrame plot method, as the following image shows:

   <img width="470" alt="image" src="https://github.com/samcandia/SQLAlchemy-Challenge/assets/145384304/1a9ea7cf-65f9-44a7-9960-6aee2637b65a">

6. Used Pandas to print the summary statistics for the precipitation data.

### Station Analysis

1. Designed a query to calculate the total number of stations in the dataset.

2. Designed a query to find the most-active stations (that is, the stations that have the most rows).

3. Designed a query that calculates the lowest, highest, and average temperatures that filters on the most-active station id found in the previous query.

4. Designed a query to get the previous 12 months of temperature observation (TOBS) data.

   <img width="479" alt="image" src="https://github.com/samcandia/SQLAlchemy-Challenge/assets/145384304/6d06d273-c6cd-4932-9e5c-30f2ace27ce6">

## Part 2: Design a Climate App

After completing the initial analysis, I designed a Flask API based on the queries that were just developed.

/

Started at the homepage and listed all the available routes.

- /api/v1.0/precipitation

- /api/v1.0/stations

- /api/v1.0/tobs

- /api/v1.0/<start> and /api/v1.0/<start>/<end>





