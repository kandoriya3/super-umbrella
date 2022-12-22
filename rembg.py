import cv2
import base64
import io

def pipeline(input_image):
    # Gaussian blur
    blur = cv2.GaussianBlur(input_image, (5, 5), 0)

    # Edge detection
    edges = cv2.Canny(blur, 75, 200)

    # Median filter
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    median = cv2.medianBlur(edges, 3)

    # Dilate
    dilate = cv2.dilate(median, kernel, iterations=5)

    # Find significant contours
    _, contours, _ = cv2.findContours(dilate, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    mask = np.zeros(input_image.shape, dtype=np.uint8)
    cv2.drawContours(mask, contours, 0, (255, 255, 255), -1)

    # Mask probable background
    mask = cv2.bitwise_not(mask)
    output_image = cv2.bitwise_and(input_image, input_image, mask=mask)

    return output_image

def process_image(input_path, output_path):
    # Load the input image
    input_image = cv2.imread(input_path)

    # Run the image processing pipeline
    output_image = pipeline(input_image)

    # Encode the output image as a PNG
    png_bytes = io.BytesIO()
    cv2.imwrite(png_bytes, output_image)

    # Return the output image as a data URL
    return "data:image/png;base64," + base64.b64encode(png_bytes.getvalue()).decode()
