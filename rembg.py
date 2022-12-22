# rembg.py

import base64
import cv2
import numpy as np
from flask import Flask, request

app = Flask(__name__)

@app.route("/rembg", methods=["POST"])
def rembg():
  # Get the data URL of the uploaded image from the request body
  data_url = request.data

  # Load the image from the data URL
  image_data = base64.b64decode(data_url.split(",")[1])
  image = cv2.imdecode(np.frombuffer(image_data, np.uint8), cv2.IMREAD_COLOR)

  # Convert the image to grayscale and apply a threshold
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

  # Find the contours of the foreground objects
  cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  cnts = cnts[0] if len(cnts) == 2 else cnts[1]

  # Create a mask with the same size as the image and fill it with white
  mask = np.ones(image.shape[:2], dtype=np.uint8) * 255

  # Draw the contours on the mask
  cv2.drawContours(mask, cnts, -1, 0, -1)

  # Apply the mask to the image
  processed_image = cv2.bitwise_and(image, image, mask=mask)

  # Encode the processed image as a JPEG and return it as a data URL
  _, jpeg_data = cv2.imencode(".jpg", processed_image)
  processed_data_url = f"data:image/jpeg;base64,{base64.b64encode(jpeg_data).decode()}"

  # Return the processed image data URL as the response
  return processed_data_url
