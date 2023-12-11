import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy 
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
import flask 
from flask import Flask , jsonify

engine = create_engine(f"sqlite:///Resources/hawaii.sqlite")
Base =automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

app = Flask(__name__)

# Listing all available routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Welcome to the Hawaii Climate API! Below are the Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start<br/>"
        f"/api/v1.0/temp/start/end<br/>"
    )

#Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value.
@app.route("/api/v1.0/precipitation")
def precipitation():
    most_recent_date = session.query(func.max(Measurement.date)).scalar()
    most_recent_date = dt.datetime.strptime(most_recent_date, '%Y-%m-%d')
    months_ago_12 = most_recent_date - dt.timedelta(days=365)
    precipitation_last12mnths = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= months_ago_12).order_by(Measurement.date).all()
    precipitation_df = pd.DataFrame(precipitation_last12mnths, columns=['Date', 'Precipitation'])
    precipitation_df.set_index('Date', inplace=True)
    precipitation = []
    for index, row in precipitation_df.iterrows():
        dateprecip = {"date": index, "prcp": row['Precipitation']}
        precipitation.append(dateprecip)
    return jsonify(precipitation)

#Return a JSON list of stations from the dataset
@app.route("/api/v1.0/stations")
def stations():
    station = session.query(Station.station).all()
    stations = list(np.ravel(station))
    return jsonify (stations)

#Query the dates and temperature observations of the most-active station for the previous year of data.
@app.route("/api/v1.0/tobs")
def tobs():
    most_recent_date = session.query(func.max(Measurement.date)).scalar()
    most_recent_date = dt.datetime.strptime(most_recent_date, '%Y-%m-%d')
    months_ago_12 = most_recent_date - dt.timedelta(days=365)
    temperature_data = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= months_ago_12).all()
    temperature = []
    for date, tobs in temperature_data:
        yeartemp = {"date": date, "tobs": tobs}
        temperature.append(yeartemp)
    return jsonify(temperature)

@app.route("/api/v1.0/temp/<start>")
def temperature_start(start):
    start_date = dt.datetime.strptime(start, '%Y-%m-%d')
    temperature_data = session.query(func.min(Measurement.tobs).label('TMIN'),func.avg(Measurement.tobs).label('TAVG'),func.max(Measurement.tobs).label('TMAX')).filter(Measurement.date >= start_date).all()
    result_dict = {
        'TMIN': temperature_data[0].TMIN,
        'TAVG': temperature_data[0].TAVG,
        'TMAX': temperature_data[0].TMAX
    }
    return jsonify(result_dict)

#Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.
# the words 'start' and 'end' will need to be replaced with a date in YYY-MM-DD format
@app.route("/api/v1.0/temp/<start>/<end>")
def temperature_start_end(start, end):
    start_date = dt.datetime.strptime(start, '%Y-%m-%d')
    end_date = dt.datetime.strptime(end, '%Y-%m-%d')

    temperature_data = session.query(func.min(Measurement.tobs).label('TMIN'),func.avg(Measurement.tobs).label('TAVG'),func.max(Measurement.tobs).label('TMAX')).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    result_dict = {
        'TMIN': temperature_data[0].TMIN,
        'TAVG': temperature_data[0].TAVG,
        'TMAX': temperature_data[0].TMAX
    }
    return jsonify(result_dict)



if __name__ == '__main__':
    app.run()
