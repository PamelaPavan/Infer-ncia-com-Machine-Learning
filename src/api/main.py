# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import xgboost as xgb
from pathlib import Path

app = FastAPI()

class Reservation(BaseModel):
    no_of_adults: int
    no_of_children: int
    no_of_weekend_nights: int
    no_of_week_nights: int
    type_of_meal_plan: str
    required_car_parking_space: int
    room_type_reserved: str
    lead_time: int
    arrival_year: int
    arrival_month: int
    arrival_date: int
    market_segment_type: str
    repeated_guest: int
    no_of_previous_cancellations: int
    no_of_previous_bookings_not_canceled: int
    no_of_special_requests: int

def season(x):
    if x in [9,10,11]:
        return 'Autumn'
    if x in [1,2,12]:
        return 'Winter'
    if x in [3,4,5]:
        return 'Spring'
    if x in [6,7,8]:
        return 'Summer'
    return x
   
@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.post('/api/v1/predict')
async def predict(reservation: Reservation):
    try:
        # Criar o DataFrame a partir dos dados de entrada
        data_dict = {
            "no_of_adults": [reservation.no_of_adults],
            "no_of_children": [reservation.no_of_children],
            "no_of_weekend_nights": [reservation.no_of_weekend_nights],
            "no_of_week_nights": [reservation.no_of_week_nights],
            "type_of_meal_plan": [reservation.type_of_meal_plan],
            "required_car_parking_space": [reservation.required_car_parking_space],
            "room_type_reserved": [reservation.room_type_reserved],
            "lead_time": [reservation.lead_time],
            "arrival_year": [reservation.arrival_year],
            "arrival_month": [reservation.arrival_month],
            "arrival_date": [reservation.arrival_date],
            "market_segment_type": [reservation.market_segment_type],
            "repeated_guest": [reservation.repeated_guest],
            "no_of_previous_cancellations": [reservation.no_of_previous_cancellations],
            "no_of_previous_bookings_not_canceled": [reservation.no_of_previous_bookings_not_canceled],
            "no_of_special_requests": [reservation.no_of_special_requests]
        }

        df = pd.DataFrame(data_dict, index=[0])
        df_copy = df.copy()

        df_copy['no_total_people'] = df_copy['no_of_adults'] + df_copy['no_of_children']
        df_copy['no_total_nights'] = df_copy['no_of_weekend_nights'] + df_copy['no_of_week_nights']
        df_copy['season_group']= df_copy['arrival_month'].apply(season)

        dummies = pd.get_dummies(df_copy[['type_of_meal_plan', 'room_type_reserved', 'market_segment_type', 'season_group']])
        df_final = pd.concat([df_copy, dummies.astype(float)], axis=1)

        df_final.drop(['type_of_meal_plan', 'room_type_reserved', 'market_segment_type', 'season_group'], inplace=True, axis=1)

        # Create a DMatrix
        dtrain = xgb.DMatrix(df_final.values)
        data_folder = Path('/app/xgboost-model')
    
        model = xgb.Booster()
        model.load_model(data_folder)

        prediction = model.predict(dtrain)
        prediction += 1

        return { "result": int(prediction)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))