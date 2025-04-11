from data_analytics.model_collection import ModelCollections

model_collection = None

def init_models():
    """Initialize models for backend"""
    global model_collection
    model_collection = ModelCollections()
    model_collection.train_all()
