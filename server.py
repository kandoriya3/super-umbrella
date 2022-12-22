from flask import Flask, render_template, request, redirect, url_for
import os
import cv2
import base64
import uuid
import rembg

app = Flask(__name__)

UPLOAD_FOLDER = '/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET'])
def index():
  return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
  if 'input-image' not in request.files:
    return redirect(url_for('index'))
  file = request.files['input-image']
  if file.filename == '':
    return redirect(url_for('index'))
  if file:
    filename = str(uuid.uuid4()) + '.jpg'
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    image = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    result = rembg.remove_background(image)
    cv2.imwrite(os.path.join(app.config['UPLOAD_FOLDER'], 'result-' + filename), result)
    with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'rb') as input_file:
      input_image = base64.b64encode(input_file.read()).decode('utf-8')
    with open(os.path.join(app.config['UPLOAD_FOLDER'], 'result-' + filename), 'rb') as result_file:
      result_image = base64.b64encode(result_file.read()).decode('utf-8')
    return render_template('result.html', input_image=input_image, result_image=result_image)

if __name__ == '__main__':
  app.run()
