from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
  if request.method == 'POST':
    # Get form data
    file = request.files['file']

    # Process file
    result = process_file(file)

    # Render result template
    return render_template('result.html', result=result)
  else:
    # Render index template
    return render_template('index.html')

def process_file(file):
  # Process file
  result = file.filename
  return result

if __name__ == '__main__':
  app.run()
