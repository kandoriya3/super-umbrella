# import the necessary libraries
from PIL import Image
from io import BytesIO
import sys

# check if the form has been submitted and a file has been uploaded
if 'photo' in sys.argv[1]:
  # create a Pillow image from the uploaded file
  image = Image.open(BytesIO(sys.argv[1]['photo'].value))

  # remove the background from the image
  image = image.convert("RGBA")
  pixdata = image.load()
  for y in range(image.size[1]):
    for x in range(image.size[0]):
      if pixdata[x, y] == (255, 255, 255, 255):
        pixdata[x, y] = (255, 255, 255, 0)
  image.save("result.png", "PNG")

  # output the resulting image as a data URI
  with open("result.png", "rb") as f:
    data = f.read()
  print("data:image/png;base64," + data.encode("base64").strip())
