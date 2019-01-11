import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
#################################################
# Database Setup
#################################################
engine = create_engine("sqlite://hawaii.sqlite", connect_args={'check_same_thread': False})

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)
# 2. Create an app, being sure to pass __name__
app = Flask(__name__)


# 3. Define what to do when a user hits the index route
@app.route("/")
def home():

    return (
        "f<p>Welcome to the Hawaii weather API!</p>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"

    )


# 4. Define what to do when a user hits the /about route
#precipitation
@app.route("/api/v1.0/precipitation")
def precipitation():
    prcp_score = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date).all()
    return jsonify(prcp_score)

# return a JSON list of stations from the dataset
@app.route("/api/v1.0/stations")
def stations():
    station_names = session.query(Measurement.station).group_by(Measurement.station).all()
    return jsonify(station_names)

#Return a JSON list of Temperature Observations (tobs) for the previous year.

@app.route("/api/v1.0/tobs")
def tobs():
    last_12_tobs = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= '2016-11-19').filter(Measurement.date <= '2017-11-19').order_by(Measurement.date).all()
    return jsonify(tobs)
#* Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
@app.route("/api/v1.0/start")
def start(date):
    start_date=session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
    filter(Measurement.date >= date).all()
    return jsonify(start_date)


@app.route("/api/v1.0/start/end")
def end(start,end):
    multi_day_temp_results =session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    return jsonify(multi_day_temp_results)

if __name__ == "__main__":
    app.run(debug=True)
