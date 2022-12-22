from flask import Flask, request, redirect, url_for, render_template
import os

app = Flask(__name__)

# Set the upload folder and allowed file types
UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Function to check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the file is part of the request
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, ignore the request
        if file.filename == '':
            return redirect(request.url)
        # If the file is allowed, save it to the uploads folder
        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))
    return render_template('index.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return render_template('result.html', input_image=url_for('static', filename='uploads/' + filename), result_image=url_for('static', filename='uploads/result_' + filename))

if __name__ == '__main__':
    app.run(debug=True)
