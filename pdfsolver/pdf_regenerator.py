
import os
import json
import numpy as np
from pdf2image import convert_from_path
from PIL import Image, ImageDraw, ImageFont
import easyocr

# Step 1: File paths
pdf_path = "/Users/dianli/Downloads/englilsh/好快_10天背完3000英语单词_加_柏莱恩 13.pdf"  # Change this to your PDF filename
output_dir = "translated_pages"
os.makedirs(output_dir, exist_ok=True)

# Step 2: OCR reader
reader = easyocr.Reader(['no'])

# Step 3: 替换词典（可以用于后处理）
substitutions = {
    'menu': 'meny'
}
# Step 4: Convert PDF to images
pages = convert_from_path(pdf_path, dpi=300)

# Step 5: Process each page with user review
for i, page in enumerate(pages):
    print(f"Processing page {i+1}/{len(pages)}")
    image = page.convert("RGB")
    image_np = np.array(image)

    # OCR
    results = reader.readtext(image_np)

    # Save OCR results for review
    review_file = f"ocr_results_page_{i+1:03}.json"

    # Load possibly edited results
    with open(review_file, 'r') as f:
        results = json.load(f)
    font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 36)

    # Draw replacements
    draw = ImageDraw.Draw(image)
    for bbox, text, _ in results:
        for word in text.split():
            cleaned = word.strip(".,:;[]()")
            if cleaned in substitutions:
                # Clean and convert coordinates
                top_left = tuple(map(float, bbox[0]))
                bottom_right = tuple(map(float, bbox[2]))
                draw.rectangle([top_left, bottom_right], fill="white")
                if cleaned[0].isupper():
                    dt = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 36)
                    draw.text(top_left, substitutions[cleaned], fill=(0, 128, 0), font=dt)
                    continue
                draw.text(top_left, substitutions[cleaned], fill=(0, 128, 0), font=font)

    # Save edited image
    output_image_path = os.path.join(output_dir, f"page_{i+1:03}.png")
    image.save(output_image_path)

# Step 6: Combine into a single PDF
#print("📦 Combining all edited pages into final PDF...")
#image_files = [os.path.join(output_dir, f) for f in sorted(os.listdir(output_dir)) if f.endswith(".png")]
#images = [Image.open(f).convert("RGB") for f in image_files]
#images[0].save("translated_output.pdf", save_all=True, append_images=images[1:])
#print("✅ PDF saved as translated_output.pdf")