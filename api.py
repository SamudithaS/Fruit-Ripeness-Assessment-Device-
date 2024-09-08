from flask import Flask, request, jsonify
import cv2
import numpy as np
import os
from roboflow import Roboflow
import logging

app = Flask(__name__)

# Initialize Roboflow API with your API key
rf = Roboflow(api_key="dE6zZPFFQwCIaDFPwGAB")
rf2 = Roboflow(api_key="Sw4eTrob1ED3VthOsHdU")
rf3 = Roboflow(api_key="dE6zZPFFQwCIaDFPwGAB")
rf4 = Roboflow(api_key="Sw4eTrob1ED3VthOsHdU")
rf5 = Roboflow(api_key="Sw4eTrob1ED3VthOsHdU")

# List of models to use for object detection
models = [
    #rf.workspace().project("carrot-pinapple").version(2).model,
    #rf.workspace().project("apple-detection-5d9rl").version(1).model,
    rf2.workspace().project("potato-gtxmy").version(1).model,
    #rf3.workspace().project("watermelon-samples").version(1).model,
    #rf4.workspace().project("tomates-gxrjf").version(7).model,
    rf.workspace().project("pineapple-d7uot").version(8).model
]

@app.route('/detect', methods=['POST'])
def detect_objects():
    try:
        image_file = request.files['image']
        image = cv2.imdecode(np.frombuffer(image_file.read(), np.uint8), -1)
        print(image_file)
        annotated_image = image.copy()

        highest_confidence_class = ""
        highest_confidence = 0
        message =""

        for model in models:
            predictions = model.predict(annotated_image, confidence=70, overlap=30).json()
            for prediction in predictions['predictions']:
                confidence = int(float(prediction['confidence']) * 100)
                if confidence > highest_confidence:
                    highest_confidence_class = prediction['class']
                    highest_confidence = confidence
        print(highest_confidence_class)
        

        if highest_confidence_class == "Un_Ripe":
            message = "Half fresh pineapple"
        elif highest_confidence_class == "Semi_Ripe":
            message = "Half fresh pineapple"
        elif highest_confidence_class == "Ripe":
            message = "Fresh pineapple"
        elif highest_confidence_class == "tomato":
            message = "Fresh tomato"
        elif highest_confidence_class == "Tomato":
            message = "Fresh Tomato"
        elif highest_confidence_class == "potato fresh 30%":
            message = "Half fresh potato"
        elif highest_confidence_class == "rotten potato":
            message = "Rotten potato"
        elif highest_confidence_class == "freshpotato":
            message = "Fresh potato"
        elif highest_confidence_class == "fresh banana":
            message = "Fresh banana"
        elif highest_confidence_class == "rotten banana":
            message = "Rotten banana"
        elif highest_confidence_class == "fresh banana 30%":
            message = "Half fresh banana"
        else:
            message = "Unknown class"


        response_data = {
            # "highest_confidence_class": highest_confidence_class,
            "confidence": highest_confidence,
            "message": message
        }
        return jsonify(response_data)

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host=os.getenv("HOST", "0.0.0.0"), port=os.getenv("PORT", 80))
