from flask import Flask, request, render_template
import rembg

app = Flask(__name__)

@app.route("/rembg", methods=["GET", "POST"])
def rembg_endpoint():
    if request.method == "POST":
        # Get the uploaded file
        file = request.files["file"]

        # Process the file using the rembg script
        processed_data_url = rembg.process_image(file)

        # Render the result template with the processed image
        return render_template("result.html", processed_data_url=processed_data_url)
    else:
        # Return a 405 error if the request method is not POST
        return "405 Not Allowed", 405

if __name__ == "__main__":
    app.run()
