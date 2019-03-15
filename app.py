import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

###################

engine = create_engine("sqlite:///Resources /hawaii.sqlite")
#conn = engine.connect()


# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Assign the station class to avariable called station 
statio = Base.classes.station 

# Assign the measurement classes to be variable called

measurement = Base.classes.measurement

# to query the server we use a session object

session = Session(bind=engine)


# 2. Create an app, being sure to pass __name__
app = Flask(__name__)


# 3. Define what to do when a user hits the index route

    
@app.route("/")
def home():
    return (
        f"<h1>Climate Analysis</h1><br/>"
        f"Available Routes:<br/>"
        )       
"""<a href="/api/v1.0/station">/api/v1.0/station(List of stations)</a><br/>"""
"""<a href="/api/v1.0/tobs">/api/v1.0/tobs (Temperature observations for the previous year)</a><br/>"""
"""<a href="/api/v1.0/precipitation">/api/v1.0/precipitation (Precipitation for the previous year)</a><br/>"""
"""<a href="/api/v1.0/2017-01-01/2017-12-31">/api/v1.0/start_date/end_date (Temperature statistics for given date range)</a><br/>"""
    
  
         
# 4. Define what to do when a user hits the /about route

@app.route("/api/v1.0/stations")
def stations():
    
     # Return a JSON list of stations from the dataset.
     # query the database for stations 
    
    station = session.query(Station.station).all ()
    
    # covenvert object to a list 
    
    station_list =[]
    for sublist in station :
        for item in sublist : 
            station_list.append (item)
            
    #return jsonfied list 
    
    return (jsonify(station_list))
    

if __name__ == "__main__":
    app.run(debug=True)
