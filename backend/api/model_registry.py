from data_analytics.model_collection import ModelCollections
from data_analytics.constant import EXAMPLE_DATA

model_collection = None

def init_models():
    """Initialize models for backend"""
    global model_collection
    model_collection = ModelCollections()
    model_collection.train_all()
    rate, count = model_collection.predict(8, EXAMPLE_DATA)
    print(f"Passenger rate: {rate} \nPassenger count: {count}")
