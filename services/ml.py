import tflite_runtime.interpreter as tf

# Path to the .tflite file
tflite_model_path = "ModelGRUBest.tflite"

# Load the TFLite model
interpreter = tf.Interpreter(model_path=tflite_model_path)
interpreter.allocate_tensors()
