import cv2
import numpy as np

def remove_background(image_path):
  # Load image
  image = cv2.imread(image_path)

  # Convert image to grayscale
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

  # Apply Gaussian blur
  blur = cv2.GaussianBlur(gray, (5,5), 0)

  # Apply edge detection
  edges = cv2.Canny(blur, 100, 200)

  # Apply median filter to remove salt and pepper noise
  median = cv2.medianBlur(edges, 5)

  # Find significant contours
  _, contours, _ = cv2.findContours(median, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

  # Create mask
  mask = np.zeros(image.shape, np.uint8)
  for c in contours:
    cv2.drawContours(mask, [c], -1, (255,255,255), -1)

  return cv2.bitwise_and(image, mask)

if __name__ == '__main__':
  # Test function
  image_path = 'image.jpg'
  result = remove_background(image_path)
  cv2.imwrite('result.jpg', result)
