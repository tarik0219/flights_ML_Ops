# flights_ML_Ops


## Dependencies
- Python 3.8+
- Install required packages using: `pip install -r requirements.txt`

## Run
- `python app.py`
- App will be accessible at `localhost:5000`

### Docker
- Build the image by executing `docker build -t flights -f Dockerfile .`
- Run the app container to get the model and prediction.csv file locally `docker run -v $(pwd):/mydata flights python3 train.py`
- Run the app container to run the api by executing `docker run -it -p 5001:5000 flights python3 app.py`
- The app will be live at `localhost:5001/prediciton`

#### Sample Post request
```JSON
{
    "airline": "Vistara",
    "source_city": "Delhi",
    "departure_time": "Afternoon",
    "stops": "one",
    "arrival_time":"Evening",
    "destination_city":"Bangalore",
    "plane_class": "Economy",
    "duration": 4.92,
    "days_left":47
}
```
### Deploy to Kubernetes
The deployment will start up 2 pods (A Pod is the atomic unit within the Kubernetes platform.) Within each of these pods a container is created from the flights image built above. In the bottom of the YAML file it defines a service of the LoadBalancer type to divide the incoming traffic between the two pods. This can be horizontally scalled by adding more pods.  