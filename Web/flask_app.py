import os
import datetime
from flask import Flask, request, jsonify
import pandas as pd
from IrrigationUtils import CropUtils
import requests
import pickle
app = Flask(__name__)

my_dir = os.path.dirname(__file__)
tree_path = os.path.join(my_dir, 'tree_clf.pkl')
normalizer_path = os.path.join(my_dir, 'normalizer.pkl')

#load tree_clf.pkl
tree_clf = pickle.load(open(tree_path, "rb"))

#load normalizer
normalizer = pickle.load(open(normalizer_path, "rb"))

def getDataFromOpenMeteo(lon, lat):
    # get the data from open meteo api
    # return the data as a json
    url = "https://api.open-meteo.com/v1/forecast?"\
        "latitude="+str(lat)+"&longitude="+str(lon)+ "&hourly=relativehumidity_2m,rain,weathercode,et0_fao_evapotranspiration,windspeed_10m&timezone=auto"
    data = requests.get(url).json()

    #use panda and get a dataframe from data["hourly"]["time"]
    df = pd.DataFrame(data["hourly"])

    #delete from time the THH:MM
    df["time"] = df["time"].str.slice(0, 10)

    #group by time and sum the values of rain, et0_fao_evapotranspiration and get the mean of windspeed_10m, relativehumidity_2m
    df = df.groupby("time").agg({"rain": "sum", "et0_fao_evapotranspiration": "sum", "windspeed_10m": "mean", "relativehumidity_2m": "mean", "weathercode": "mean"})

    return df


@app.route('/')
def index():
    return "Non dovresti essere qui!"

@app.route('/getIrrigationDecision', methods=['GET'])
def getIrrigationDecision():
    # get the value of the key len and lat from the get Request and convert them to float
    lon = float(request.args.get('lon'))
    lat = float(request.args.get('lat'))

    #get the type of the crop
    crop = request.args.get('crop')

    #get the stage of growth of the crop
    stage = request.args.get('growthStage')

    #get the data from open meteo api
    df = getDataFromOpenMeteo(lon, lat)
    cropInfo = CropUtils(crop, stage)


    #for every row in the dataframe add the value of Kc to the dataframe
    for index, row in df.iterrows():
        df.loc[index, "Kc"] = cropInfo.calculateEstimatedKc(row["windspeed_10m"], row["relativehumidity_2m"])

    #change the name of the column et0_fao_evapotranspiration to et0_fao_evapotranspiration (mm)
    df = df.rename(columns={"et0_fao_evapotranspiration": "et0_fao_evapotranspiration (mm)",
                            "rain": "rain (mm)",
                            "relativehumidity_2m": "relativehumidity_2m (%)",
                            "windspeed_10m": "windspeed_10m (km/h)",
                            "weathercode": "weathercode (wmo code)"
                            })


    #swap windspeed_10m (km/h) and rain(mm)
    data = df[["et0_fao_evapotranspiration (mm)", "rain (mm)", "windspeed_10m (km/h)", "relativehumidity_2m (%)", "weathercode (wmo code)", "Kc"]]

    #normalize daPredire
    daPredire = normalizer.transform(data)

    irrigationDecision = tree_clf.predict(daPredire)

    #itera su irrigationDecision
    decisione = []

    for i in range(len(irrigationDecision)):
        if irrigationDecision[i] == 1:
            decisione.append(1)
        elif irrigationDecision[i] == 2:
            decisione.append(2)
        elif irrigationDecision[i] == 3:
            decisione.append(3)
        else:
            decisione.append(0)

    result = {
        "longitudine": lon,
        "latitudine": lat,
        "crop": crop,
        "stage": stage,
        "irrigationLevel": decisione
    }
    json = jsonify(result)
    
    return json

if __name__ == '__main__':
    app.run()
