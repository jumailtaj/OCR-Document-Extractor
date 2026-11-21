
def cleaned_text(texts, scores, polys):

    clean_text = []
    clean_score = []
    clean_polys = []

    # Step 1: Clean and filter OCR detections
    for text, score, poly in zip(texts, scores, polys):

        # Convert text to string and remove leading/trailing spaces
        text = str(text).strip()

        # Normalize multiple spaces into single spaces
        text = " ".join(text.split())

        # Remove empty text
        if not text:
            continue

        # Remove low-confidence detections
        if score < 0.90:
            continue

        # Remove single-character detections
        if len(text) < 2:
            continue

        # Store cleaned detections
        clean_text.append(text)
        clean_score.append(score)
        clean_polys.append(poly)

    return clean_text, clean_score, clean_polys
