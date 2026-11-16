
def cleaned_text(texts, scores, polys):

    clean_text = []
    clean_score = []
    clean_polys = []

    # Step 1: Clean and filter OCR detections
    for text, score, poly in zip(texts, scores, polys):

        # Remove leading and trailing spaces
        text = text.strip()

        # Normalize multiple spaces
        text = " ".join(text.split())

        # Remove empty text, low-confidence detections
        # and single-character detections
        if not text or score < 0.90 or len(text) < 2:
            continue

        clean_text.append(text)
        clean_score.append(score)
        clean_polys.append(poly)

    return clean_text, clean_score, clean_polys


def line_organizer(texts, scores, polys):

    detections = []

    # Step 1: Calculate coordinates for each detection
    for text, score, poly in zip(texts, scores, polys):

        xs = [point[0] for point in poly]
        ys = [point[1] for point in poly]

        left_x = min(xs)
        right_x = max(xs)

        top_y = min(ys)
        bottom_y = max(ys)

        center = (top_y + bottom_y) / 2
        height = bottom_y - top_y

        # Store detection information
        detections.append({
            "text": text,
            "score": score,
            "poly": poly,
            "center": center,
            "height": height,
            "left_x": left_x,
            "right_x": right_x
        })

    # Step 2: Sort detections from top to bottom
    detections.sort(key=lambda item: item["center"])

    lines = []

    # Step 3: Group detections into lines
    for item in detections:

        # Create the first line
        if not lines:
            lines.append([item])
            continue

        # Get the latest line
        current_line = lines[-1]

        # Calculate the average vertical center
        line_center = sum(
            word["center"] for word in current_line
        ) / len(current_line)

        # Calculate vertical tolerance
        tolerance = max(
            10,
            min(item["height"], current_line[0]["height"]) * 0.5
        )

        # Compare vertical positions
        difference = abs(item["center"] - line_center)

        if difference <= tolerance:

            # Same line
            current_line.append(item)

        else:

            # New line
            lines.append([item])

    # Step 4: Sort each line from left to right
    for line in lines:

        line.sort(key=lambda item: item["left_x"])

    return lines



