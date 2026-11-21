
from paddleocr import PaddleOCR

from structuring.cleaner import cleaned_text
from structuring.lines_organiging import (
    line_organizer,
    merge_multiline_text
)


# 1. Initialize OCR
ocr = PaddleOCR(
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False,
    engine="paddle"
)


# 2. Extract text from image
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
    polys = data["rec_polys"]


    # 4. Clean OCR detections
    clean_text, clean_score, clean_polys = cleaned_text(
        texts,
        scores,
        polys
    )


    # 5. Group horizontal text
    organized_lines = line_organizer(
        clean_text,
        clean_score,
        clean_polys
    )


    # 6. Merge multiline text
    merged_lines = merge_multiline_text(organized_lines)


    # 7. Print final merged text
    print("\n========== FINAL MERGED TEXT ==========\n")

    for line_number, line in enumerate(merged_lines, start=1):

        line_text = " ".join(
            item["text"] for item in line
        )

        print(f"Line {line_number}: {line_text}")


    # 8. Print detailed information
    print("\n========== DETAILED INFORMATION ==========\n")

    for line_number, line in enumerate(merged_lines, start=1):

        print(f"\nLine {line_number}")

        for item in line:

            print("Text:", item["text"])
            print("Confidence:", item["score"])
            print("Coordinates:", item["poly"])
            print("Center Y:", item["center"])
            print("Left X:", item["left_x"])
