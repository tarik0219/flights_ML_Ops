from typing import Literal
from flask import Flask,request,jsonify,Response
from joblib import load
from pydantic import BaseModel,ValidationError
import pandas as pd
from typing import Literal

app = Flask(__name__)

class Flight(BaseModel):
    airline: Literal['Vistara', 'SpiceJet', 'AirAsia', 'Air_India', 'Indigo', 'GO_FIRST']
    source_city: Literal['Delhi', 'Bangalore', 'Mumbai', 'Kolkata', 'Chennai', 'Hyderabad']
    departure_time: Literal['Afternoon', 'Early_Morning', 'Morning', 'Night', 'Evening', 'Late_Night']
    stops: Literal['one', 'zero', 'two_or_more']
    arrival_time: Literal['Evening', 'Early_Morning', 'Night', 'Morning', 'Afternoon', 'Late_Night']
    destination_city:Literal['Bangalore', 'Chennai', 'Mumbai', 'Hyderabad', 'Delhi', 'Kolkata']
    plane_class: Literal['Economy', 'Business']
    duration:float
    days_left:float

def dict_to_dict_list(dict):
    cat_cols = ['airline', 'source_city', 'departure_time', 'stops', 'arrival_time', 'destination_city', 'plane_class']
    new_dict = {}
    for key,value in dict.items():
        if key == 'plane_class':
            new_dict[f'class_{value}'] = 1
        elif key in cat_cols:
            new_dict[f'{key}_{value}']= 1
        else:
            new_dict[key] = value
    return new_dict

@app.route('/prediction',methods=['POST'])
def predict_model():
    model = load("model.joblib")
    if request.method == 'POST':
        request_data = request.get_json()
        try:
            Flight(**request_data)
            request_data = dict_to_dict_list(request_data)
            predict = pd.DataFrame(columns=['duration', 'days_left', 'airline_AirAsia',
       'airline_Air_India', 'airline_GO_FIRST', 'airline_Indigo',
       'airline_SpiceJet', 'airline_Vistara', 'source_city_Bangalore',
       'source_city_Chennai', 'source_city_Delhi', 'source_city_Hyderabad',
       'source_city_Kolkata', 'source_city_Mumbai', 'departure_time_Afternoon',
       'departure_time_Early_Morning', 'departure_time_Evening',
       'departure_time_Late_Night', 'departure_time_Morning',
       'departure_time_Night', 'stops_one', 'stops_two_or_more', 'stops_zero',
       'arrival_time_Afternoon', 'arrival_time_Early_Morning',
       'arrival_time_Evening', 'arrival_time_Late_Night',
       'arrival_time_Morning', 'arrival_time_Night',
       'destination_city_Bangalore', 'destination_city_Chennai',
       'destination_city_Delhi', 'destination_city_Hyderabad',
       'destination_city_Kolkata', 'destination_city_Mumbai', 'class_Business',
       'class_Economy'])
            predict = predict.append(request_data, ignore_index=True)
            predict = predict.fillna(0)
            X = predict.to_numpy()
            result = model.predict(X)
            return jsonify({"price": int(result[0])}) , 200
        except ValidationError as e:
            return jsonify({"error": str(e)}) , 400
    

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

