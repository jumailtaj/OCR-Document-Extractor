from paddleocr import PaddleOCR

# 1. Initialize OCR
ocr = PaddleOCR(
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False,
    engine="paddle"
)

# 2. Process the image
work = ocr.predict(
    r"C:\Users\Victu\OneDrive\Desktop\python\projects\OCR-Document-Extractor\samples\boarding_pass.jpg"
)

# Initialize counter
count = 0

# 3. Process OCR results
for page in work:

    data = page.json

    if "res" in data:
        data = data["res"]

    texts = data["rec_texts"]
    scores = data["rec_scores"]

    

    for text, score in zip(texts, scores):

        count = count + 1
        print(count)
        print(f"Text: {text}")
        print(f"accuracy: {score:.2%}")
        print("----------------")
