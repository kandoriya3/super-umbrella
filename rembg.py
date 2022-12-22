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

  # Step 1: Gaussian Blur
  image = cv2.GaussianBlur(image, (5, 5), 0)

  # Step 2: Edge Detection
  edges = cv2.Canny(image, 50, 150, apertureSize=3)

  # Step 3: Filter Out Salt and Pepper Noise using Median Filter
  edges = cv2.medianBlur(edges, 3)

  # Step 4: Find Significant Contours
  cnts, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

  # Step 5: Masking Probable Background
  mask = np.zeros_like(image)
  cv2.drawContours(mask, cnts, -1, (255, 255, 255), -1)

  # Apply the mask to the image
  processed_image = cv2.bitwise_and(image, mask)

  # Set the dimensions of the processed image to match the original image
  processed_image = cv2.resize(processed_image, (image.shape[1], image.shape[0]))

  # Encode the processed image as a PNG and return it as a data URL
  _, png_data = cv2.imencode(".png", processed_image)
  processed_data_url = f"data:image/png;base64,{base64.b64encode(png_data).decode()}"

  # Return the processed image data URL as the response
  return processed_data_url
