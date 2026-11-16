from paddleocr import PaddleOCR
from structuring.cleaner import cleaned_text,line_organizer


# Step 1: Initialize OCR
ocr = PaddleOCR(
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False,
    engine="paddle"
)


# Step 2: Process the image
work = ocr.predict(
    r"C:\Users\Victu\OneDrive\Desktop\python\projects\OCR-Document-Extractor\samples\boarding_pass.jpg"
)


# Step 3: Process OCR results
for page in work:

    data = page.json

    if "res" in data:
        data = data["res"]

    texts = data["rec_texts"]
    scores = data["rec_scores"]
    polys = data["rec_polys"]


    # Step 4: Clean OCR detections
    clean_text, clean_score, clean_polys = cleaned_text(
        texts,
        scores,
        polys
    )


    # Step 5: Organize detections into lines
    organized_lines = line_organizer(
        clean_text,
        clean_score,
        clean_polys
    )


    # Step 6: Print organized text
    print("\n========== ORGANIZED TEXT ==========\n")

    for line_number, line in enumerate(organized_lines, start=1):

        line_text = " ".join(
            item["text"] for item in line
        )

        print(f"Line {line_number}: {line_text}")


    # Step 7: Print detection details
    print("\n========== DETECTION DETAILS ==========\n")

    for line_number, line in enumerate(organized_lines, start=1):

        print(f"\nLine {line_number}")

        for item in line:

            print("Text:", item["text"])
            print("Confidence:", item["score"])
            print("Coordinates:", item["poly"])
            print("Center Y:", item["center"])
            print("Left X:", item["left_x"])
            print("-------------------------")
