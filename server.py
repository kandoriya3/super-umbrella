from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
  if request.method != 'POST':
    # Render index template
    return render_template('index.html')
  # Get form data
  file = request.files['file']

  # Process file
  result = process_file(file)

  # Render result template
  return render_template('result.html', result=result)

def process_file(file):
  return file.filename

if __name__ == '__main__':
  app.run()
