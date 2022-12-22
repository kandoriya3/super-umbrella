from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/process', methods=['GET', 'POST'])
def index():
  if request.method == 'POST':
    # Get form data
    file = request.files['file']
    print(f'Received file: {file}')  # Debug line

    # Process file
    result = process_file(file)
    print(f'Result: {result}')  # Debug line

    # Render result template
    return render_template('result.html', result=result)
  else:
    # Render index template
    return render_template('index.html')

def process_file(file):
  # Debug line
  import pdb; pdb.set_trace()

  # Process file
  result = file.filename
  return result

if __name__ == '__main__':
  app.run()
