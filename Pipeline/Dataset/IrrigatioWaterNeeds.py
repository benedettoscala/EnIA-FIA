import datetime
import random

import pandas

class CropWaterNeeds:
    CropType = ["Barley", "Bean", "Cabbage", "Carrot", "Cotton", "Cucumber", "Eggplant", "Grain", "Lentil", "Lettuce"]
    GrowthType = ["InitialStage", "CropDevStage", "MidSeasonStage", "LateSeasonStage"]
    
    DurationGrowth = {
        "Barley":{"InitialStage":15, "CropDevStage": 25, "MidSeasonStage": 50, "LateSeasonStage": 30, "Total": 120},
        "Bean": {"InitialStage": 15, "CropDevStage": 25, "MidSeasonStage": 25, "LateSeasonStage": 10, "Total": 75},
        "Cabbage": {"InitialStage": 20, "CropDevStage": 25, "MidSeasonStage": 60, "LateSeasonStage": 15, "Total": 120},
        "Carrot": {"InitialStage": 20, "CropDevStage": 30, "MidSeasonStage": 30, "LateSeasonStage": 70, "Total": 150},
        "Cotton": {"InitialStage": 30, "CropDevStage": 50, "MidSeasonStage": 55, "LateSeasonStage": 45, "Total": 180},
        "Cucumber": {"InitialStage": 20, "CropDevStage": 30, "MidSeasonStage": 40, "LateSeasonStage": 15, "Total": 105},
        "Eggplant": {"InitialStage": 30, "CropDevStage": 40, "MidSeasonStage": 40, "LateSeasonStage": 20, "Total": 130},
        "Grain" : {"InitialStage": 20, "CropDevStage": 30, "MidSeasonStage": 60, "LateSeasonStage": 40, "Total": 150},
        "Lentil" : {"InitialStage": 20, "CropDevStage": 30, "MidSeasonStage": 60, "LateSeasonStage": 40, "Total": 150},
        "Lettuce": {"InitialStage": 20, "CropDevStage": 30, "MidSeasonStage": 15, "LateSeasonStage": 10, "Total": 75}
    }

    CropFactor = {
        "Barley": {"InitialStage": 0.35, "CropDevStage": 0.75, "MidSeasonStage": 1.15, "LateSeasonStage": 0.45},
        "Bean": {"InitialStage": 0.35, "CropDevStage": 0.70, "MidSeasonStage": 1.10, "LateSeasonStage": 0.90},
        "Cabbage":{"InitialStage": 0.45, "CropDevStage": 0.75, "MidSeasonStage": 1.05, "LateSeasonStage": 0.90},
        "Carrot":{"InitialStage": 0.45, "CropDevStage": 0.75, "MidSeasonStage": 1.05, "LateSeasonStage": 0.90},
        "Cotton":{"InitialStage": 0.45, "CropDevStage": 0.75, "MidSeasonStage": 1.15, "LateSeasonStage": 0.75},
        "Cucumber":{"InitialStage": 0.45, "CropDevStage": 0.70, "MidSeasonStage": 0.90, "LateSeasonStage": 0.75},
        "Eggplant":{"InitialStage": 0.45, "CropDevStage": 0.75, "MidSeasonStage": 1.15, "LateSeasonStage": 0.80},
        "Grain":{"InitialStage": 0.35, "CropDevStage": 0.75, "MidSeasonStage": 1.10, "LateSeasonStage": 0.65},
        "Lentil": {"InitialStage": 0.45, "CropDevStage": 0.75, "MidSeasonStage": 1.10, "LateSeasonStage": 0.50},
        "Lettuce": {"InitialStage": 0.45, "CropDevStage": 0.60, "MidSeasonStage": 1.00, "LateSeasonStage": 0.90}
    }
    
    def calculateKc( Kc, windspeed, humidity):
        cropK = Kc
        if windspeed < 2 and humidity > 80:
            Kc = Kc - 0.5
        if humidity < 50 and windspeed > 5:
            Kc = Kc + 0.5
        return cropK
    
    def calculateEffectivePrecipitation(precipitation):
        pe = 0
        if precipitation > 2.5:
            pe = (0.8*precipitation - 0.33)
        elif precipitation > 0:
            pe =  (0.6*precipitation - 0.83)
        else:
            pe = 0
        if pe < 0:
            pe = 0
        return pe
    
    
    def calculateIrrigationWaterNeeds(crop, stageOfGrowth, windspeed, humidity, precipitation, ETo):
        estimatedKc = CropWaterNeeds.calculateKc(CropWaterNeeds.CropFactor[crop][stageOfGrowth], windspeed, humidity)
        effectivePrecipiation = CropWaterNeeds.calculateEffectivePrecipitation(precipitation)
        ETcrop = estimatedKc * ETo
        return ETcrop - effectivePrecipiation
        


meteo = pandas.read_csv("C:/Users/scala/OneDrive/Desktop/FIA/EnIA/DatasetIrrigazione.csv")


#cut the last 6 characters from the date
meteo['time'] = meteo['time'].str[:-6]

#Combine each day into a single entry, and add for each day the value of evapotranspiration and that of precipitation, take one value ov weather code per time
meteo = meteo.groupby(['time']).agg({'surface_pressure (hPa)': 'mean', 'soil_moisture_0_to_7cm (m³/m³)':'mean' ,'et0_fao_evapotranspiration (mm)': 'sum', 'rain (mm)': 'sum', 'windspeed_10m (km/h)': 'mean', 'relativehumidity_2m (%)': 'mean', 'temperature_2m (°C)': 'mean', 'soil_temperature_0_to_7cm (°C)': 'mean', 'cloudcover (%)': 'mean', 'shortwave_radiation (W/m²)': 'sum', 'weathercode (wmo code)': 'first'})
#meteo = meteo.groupby(['time']).agg({'et0_fao_evapotranspiration (mm)': 'sum', 'rain (mm)': 'sum', 'windspeed_10m (km/h)': 'mean', 'relativehumidity_2m (%)': 'mean'})


print(meteo.head())
#get csv from meteo
meteo.to_csv("C:/Users/scala/OneDrive/Desktop/FIA/EnIA/irrigazione.csv")


#Add an attribute named crop for each entry where you assign a random crop type value
meteo['crop'] = meteo.apply(lambda row: CropWaterNeeds.CropType[random.randint(0,9)], axis=1)

#Add an attribute named stageOfGrowth for each entry where you assign a random stage of growth value
meteo['stageOfGrowth'] = meteo.apply(lambda row: CropWaterNeeds.GrowthType[random.randint(0,3)], axis=1)

#Add an attribute named Kc for each entry where you assign the value of the function calculateKc
meteo['Kc'] = meteo.apply(lambda row: CropWaterNeeds.calculateKc(CropWaterNeeds.CropFactor[row['crop']][row['stageOfGrowth']], row['windspeed_10m (km/h)'], row['relativehumidity_2m (%)']), axis=1)

#Add an attribute named irrigationWaterNeeds for each entry where you assign the value of the function calculate
meteo['irrigationWaterNeeds'] = meteo.apply(lambda row: CropWaterNeeds.calculateIrrigationWaterNeeds(row['crop'], row['stageOfGrowth'], row['windspeed_10m (km/h)'], row['relativehumidity_2m (%)'], row['rain (mm)'], row['et0_fao_evapotranspiration (mm)']), axis=1)

#add an attribute named irrigation where you assign 1 when irrigationwaterneeds is over 0, 1 when it is over 1.5, 2 when it is over 3, 0 when it is under 0
meteo['irrigation'] = meteo.apply(lambda row: 0 if row['irrigationWaterNeeds'] < 0 else 1 if row['irrigationWaterNeeds'] < 1.5 else 2 if row['irrigationWaterNeeds'] < 3 else 3, axis=1)

#drop irrigationWaterNeeds
meteo = meteo.drop(columns=['irrigationWaterNeeds'])


#approximates each value in the table to 2 decimal places
meteo = meteo.round(2)


#get a csv from meteo
meteo.to_csv("C:/Users/scala/OneDrive/Desktop/FIA/EnIA/DatasetEnIA.csv")


#print(meteo.head())