# rembg.py

from flask import Flask, request
from PIL import Image

app = Flask(__name__)

@app.route("/rembg", methods=["POST"])
def rembg():
  # Get the data URL of the uploaded image from the request body
  data_url = request.data

  # Load the image from the data URL
  image = Image.open(BytesIO(base64.b64decode(data_url)))

  # Process the image to remove the background
  # (Replace this with your own code using OpenCV or Pillow)
  processed_image = image.copy()

  # Save the processed image as a data URL
  buffer = BytesIO()
  processed_image.save(buffer, format="JPEG")
  processed_data_url = f"data:image/jpeg;base64,{base64.b64encode(buffer.getvalue()).decode()}"

  # Return the processed image data URL as the response
  return processed_data_url
