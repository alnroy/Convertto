import cv2
import os

def preprocess_image(image_path):
    """
    Preprocesses an image to make handwriting more OCR-friendly.
    Returns path of the new preprocessed image.
    """
    # Read as grayscale
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Resize to make letters bigger
    img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    # Denoise
    img = cv2.bilateralFilter(img, 9, 75, 75)

    # Increase contrast & binarize
    img = cv2.adaptiveThreshold(
        img, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 31, 2
    )

    # Save processed version
    base, ext = os.path.splitext(image_path)
    processed_path = base + "_pre.png"
    cv2.imwrite(processed_path, img)

    return processed_path
