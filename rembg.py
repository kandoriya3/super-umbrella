import cv2
import numpy as np

def gaussian_blur(image, kernel_size=5):
  return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)

def edge_detection(image, threshold1=50, threshold2=150):
  return cv2.Canny(image, threshold1, threshold2)

def median_filter(image, kernel_size=3):
  return cv2.medianBlur(image, kernel_size)

def find_contours(image):
  _, contours, _ = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  return contours

def mask_background(image, contours):
  mask = np.zeros_like(image)
  cv2.drawContours(mask, contours, -1, 255, -1)
  return mask

def remove_background(image):
  # Step 1: Gaussian Blur
  image = gaussian_blur(image)
  
  # Step 2: Edge Detection
  edges = edge_detection(image)
  
  # Step 3: Filter Out Salt and Pepper Noise using Median Filter
  edges = median_filter(edges)
  
  # Step 4: Find Significant Contours
  contours = find_contours(edges)
  
  # Step 5: Masking Probable Background
  mask = mask_background(image, contours)
  
  # Apply mask to input image
  result = cv2.bitwise_and(image, mask)
  
  return result
