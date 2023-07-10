import tensorflow as tf

# Path to the .tflite file
tflite_model_path = "./ModelPrediksi.tflite"

# Load the TFLite model
interpreter = tf.lite.Interpreter(model_path=tflite_model_path)
interpreter.allocate_tensors()
