from paddleocr import PaddleOCR
from structuring.cleaner import cleaned_text,line_organizer



ocr = PaddleOCR(
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False,
    engine="paddle"
)


work = ocr.predict(
    r"C:\Users\Victu\OneDrive\Desktop\python\projects\OCR-Document-Extractor\samples\Screenshot.png"
)



for page in work:

    data = page.json

    if "res" in data:
        data = data["res"]

    texts = data["rec_texts"]
    scores = data["rec_scores"]
    polys = data["rec_polys"]



    clean_text, clean_score, clean_polys = cleaned_text(
        texts,
        scores,
        polys
    )



    organized_lines = line_organizer(
        clean_text,
        clean_score,
        clean_polys
    )




    for line_number, line in enumerate(organized_lines, start=1):

        line_text = " ".join(
            item["text"] for item in line
        )

        print(f"Line {line_number}: {line_text}")




    for line_number, line in enumerate(organized_lines, start=1):

        print(f"\nLine {line_number}")

        for item in line:

            print("Text:", item["text"])
            print("Confidence:", item["score"])
            print("Coordinates:", item["poly"])
            print("Center Y:", item["center"])
            print("Left X:", item["left_x"])
