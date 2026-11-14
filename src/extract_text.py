from paddleocr import PaddleOCR
from structuring.json_builder import cleaned_text

# 1. Initialize OCR
ocr = PaddleOCR(
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False,
    engine="paddle"
)

# 2. Process the image
work = ocr.predict(
    r"C:\Users\Victu\OneDrive\Desktop\python\projects\OCR-Document-Extractor\samples\Screenshot.png"
)


# 3. Process OCR results
for page in work:

    data = page.json

    if "res" in data:
        data = data["res"]

    texts = data["rec_texts"]
    scores = data["rec_scores"]

    clean_text, clean_score = cleaned_text(texts, scores)

    for text in clean_text:
        print(text)