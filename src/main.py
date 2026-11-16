from paddleocr import PaddleOCR

ocr = PaddleOCR(
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False,
    engine="paddle"
)

work = ocr.predict(
    r"C:\Users\Victu\OneDrive\Desktop\python\projects\OCR-Document-Extractor\samples\boarding_pass.jpg"
)

for page in work:
    data = page.json

    print(data["rec_polys"])
    