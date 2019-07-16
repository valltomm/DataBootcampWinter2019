# Step 2 - Climate App 
# Use FLASK to create your routes.

#import dependencies
from flask import Flask, jsonify
import datetime as dt
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Database Setup
engine = create_engine("sqlite:///Hawaii.sqlite")
# reflect the database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Save reference to the table
Station = Base.classes.station
Measurement = Base.classes.measurement
# Create our session (link) from Python to the DB
session = Session(engine)

#Flask setup 
app = Flask(__name__)

#Home routes / 
@app.route("/")
def home():
    return(
        f"Available Routes:<br/>"
        f"<br/>"

        f"1) List of prior year rain totals from all stations<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"<br/>"

        f"2) List of Station numbers and names<br/>"
        f"/api/v1.0/stations<br/>"
        f"<br/>"

        f"3) List of prior year temperatures from all stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<br/>"

        f"4) When given the start date as YYYY-MM-DD, calculates the MIN/AVG/MAX temperature for all dates greater than and equal to the start date<br/>"
        f"/api/v1.0/<start><br/>"
        f"<br/>"

        f"5) When given the start and end date as YYYY-MM-DD/YYYY-MM-DD, calculate the MIN/AVG/MAX temperature for dates between the start and end date inclusive<br/>"
        f"/api/v1.0/<start><end><br/>"
    )


#/api/v1.0/precipitation
# Convert the query results to a Dictionary using date as the key and prcp as the value.
# (query to retrieve the last 12 months of precipitation data)
# Return the JSON representation of your dictionary.

@app.route("/api/v1.0/precipitation")
def precipitation():
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    query_date = dt.datetime(2017, 8, 23) - dt.timedelta(days=365)
    scores = session.query(Measurement.date, Measurement.prcp).order_by(Measurement.date.desc()).filter(Measurement.date >= query_date.date()).all()

    last_yr_rain = []
    for date, prcp in scores:
        rain = {}
        rain["date"] = date
        rain["prcp"] = prcp
        last_yr_rain.append(rain)

    return jsonify(last_yr_rain)

# Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    stations_query = session.query(Station.name, Station.station).all()
    station_list = list(np.ravel(stations_query))

    return jsonify(station_list)


# query for the dates and temperature observations from a year from the last data point.
# Return a JSON list of Temperature Observations (tobs) for the previous year.

@app.route("/api/v1.0/tobs")
def tobs():
    query_date = dt.datetime(2017, 8, 23) - dt.timedelta(days=365)
    temp_results = session.query(Measurement.date, Measurement.station, Measurement.tobs).filter(Measurement.date >= query_date.date()).all()
    temp_list = list(np.ravel(temp_results))
    
    return jsonify(temp_list)

# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
# When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
# When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.

@app.route("/api/v1.0/<start>")
def startdate(start):

    start_date= dt.datetime.strptime(start, '%Y-%m-%d')
    last_year = dt.timedelta(days=365)
    start = start_date-last_year
    end =  dt.date(2017, 8, 23)
    trip_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    trip = list(np.ravel(trip_data))
    return jsonify(trip)


@app.route("/api/v1.0/<start>/<end>")
def startend(start,end):

    start_date= dt.datetime.strptime(start, '%Y-%m-%d')
    end_date= dt.datetime.strptime(end,'%Y-%m-%d')
    last_year = dt.timedelta(days=365)
    start = start_date-last_year
    end = end_date-last_year
    trip_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    trip = list(np.ravel(trip_data))
    return jsonify(trip)

if __name__ == "__main__":
    app.run(debug=True)