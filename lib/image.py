import cv2
import pytesseract

def preprocess_cropped_image(input_image, roi, is_darkfont=True, has_blur=False):
    img = input_image.copy()
    # Crop the image based on ROI
    x, y, w, h = roi
    cropped_image = img[y:y+h, x:x+w]
    
    # Convert to grayscale
    gray_image = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
    
    if has_blur:
        gray_image = cv2.medianBlur(gray_image, 3)
    
    # Improved preprocessing for better OCR accuracy
    threshold_mode = cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    if (is_darkfont): 
        threshold_mode = cv2.THRESH_BINARY + cv2.THRESH_OTSU
    
    _, binary_image = cv2.threshold(gray_image, 0, 255, threshold_mode)
    
    return binary_image

def read_ocr_from_image(image, config=""):
    return pytesseract.image_to_string(image, config=config)

def read_image(captured_image, processed_image_data, parameters=None):
    roi = list(processed_image_data["roi"])
    replaced = 0
    if parameters and len(roi):
        for i in range(len(roi)):
            if type(roi[i]).__name__ == 'str':
                if replaced < len(parameters):
                    roi[i] = parameters[replaced]
                    replaced = replaced + 1
    processed_image = preprocess_cropped_image(captured_image, tuple(roi), processed_image_data["is_darkfont"], processed_image_data["has_blur"])
    return read_ocr_from_image(processed_image, processed_image_data["character_white_list"])