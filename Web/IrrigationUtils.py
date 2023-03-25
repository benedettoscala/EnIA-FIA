class CropUtils:
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
    
    def calculateEstimatedKc(self, windspeed, humidity):
        estimatedCropFactor = self.cropFactor
        if windspeed < 2 and humidity > 80:
            estimatedCropFactor = estimatedCropFactor - 0.5
        if humidity < 50 and windspeed > 5:
            estimatedCropFactor = estimatedCropFactor + 0.5
        return estimatedCropFactor
    
    def getETCrop(self, ETo, windspeed, humidity):
        return self.calculateEstimatedKc(windspeed,humidity) * ETo
    
    def __init__(self, cropType, growthType):
        self.cropType = cropType
        self.growthType = growthType
        self.cropFactor = self.CropFactor[cropType][growthType]
        
