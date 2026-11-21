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

print(work)
