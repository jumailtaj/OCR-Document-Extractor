def cleaned_text(texts, scores):

    clean_text = []
    clean_score = []

    for text, score in zip(texts, scores):

        # Remove leading and trailing spaces
        text = text.strip()

        # Normalize multiple spaces
        text = " ".join(text.split())


        # Remove empty text or low-confidence detections
        if not text or score < 0.90 or len(text) < 2 :
            continue

        clean_text.append(text)
        clean_score.append(score)

    return clean_text, clean_score

    

