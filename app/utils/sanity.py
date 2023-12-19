import tensorflow as tf

def status_gpu_check():
    gpus = tf.config.list_physical_devices('GPU')
    if gpus:
        return {"api_status":"Healthy","gpu_status":"Available"}
    else:
        return {"api_status":"Healthy","gpu_status":"Unavailable"}