import os
import json
import numpy as np
from pdf2image import convert_from_path
import easyocr

# This script extracts content from an image and generates a JSON-formatted document.
# Step 1: File paths
pdf_path = "path/p8.pdf"  # Change this to your PDF filename
output_dir = "translated_pages"
os.makedirs(output_dir, exist_ok=True)

# Step 2: OCR reader
reader = easyocr.Reader(['no'])

# Step 3: Convert PDF to images
pages = convert_from_path(pdf_path, dpi=300)

# Step 4: Process each page with user review
for i, page in enumerate(pages):
    print(f"Processing page {i+1}/{len(pages)}")
    image = page.convert("RGB")
    image_np = np.array(image)

    # OCR
    results = reader.readtext(image_np)

    # Save OCR results for review
    review_file = f"ocr_results_page_{i+1:03}.json"
    with open(review_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    print(f"🔍 OCR results saved to {review_file}")
