
def line_organizer(texts, scores, polys):

    detections = []

    for text, score, poly in zip(texts, scores, polys):

        xs = [point[0] for point in poly]
        ys = [point[1] for point in poly]

        left_x = min(xs)
        right_x = max(xs)

        top_y = min(ys)
        bottom_y = max(ys)

        center = (top_y + bottom_y) / 2
        height = bottom_y - top_y

        detections.append({
            "text": text,
            "score": score,
            "poly": poly,
            "center": center,
            "height": height,
            "left_x": left_x,
            "right_x": right_x
        })

    # Sort detections from top to bottom
    detections.sort(key=lambda item: item["center"])

    lines = []

    for item in detections:

        if not lines:
            lines.append([item])
            continue

        current_line = lines[-1]

        line_center = sum(
            word["center"] for word in current_line
        ) / len(current_line)

        tolerance = max(
            10,
            min(item["height"], current_line[0]["height"]) * 0.5
        )

        difference = abs(item["center"] - line_center)

        if difference <= tolerance:
            current_line.append(item)
        else:
            lines.append([item])

    # Sort words from left to right
    for line in lines:
        line.sort(key=lambda item: item["left_x"])

    return lines


def merge_multiline_text(lines, max_x_difference=25, max_vertical_gap=15):

    # Flatten lines into individual detections
    items = [
        (line_index, item)
        for line_index, line in enumerate(lines)
        for item in line
    ]

    # Sort from top to bottom
    items.sort(
        key=lambda entry: entry[1]["center"]
    )

    merged_items = []

    for line_index, item in items:

        left_x = item["left_x"]
        top_y = min(point[1] for point in item["poly"])
        bottom_y = max(point[1] for point in item["poly"])

        matched = False

        for previous in reversed(merged_items):

            previous_left = previous["_column_left_x"]

            previous_bottom = max(
                point[1] for point in previous["poly"]
            )

            # Check whether both detections start at similar X positions
            same_column = (
                abs(left_x - previous_left) <= max_x_difference
            )

            # Check vertical distance
            vertical_gap = top_y - previous_bottom

            close_enough = (
                0 <= vertical_gap <= max_vertical_gap
            )

            if same_column and close_enough:

                # Merge text
                previous["text"] += " " + item["text"]

                # Merge coordinates
                all_xs = (
                    [point[0] for point in previous["poly"]]
                    + [point[0] for point in item["poly"]]
                )

                all_ys = (
                    [point[1] for point in previous["poly"]]
                    + [point[1] for point in item["poly"]]
                )

                new_left = min(all_xs)
                new_right = max(all_xs)
                new_top = min(all_ys)
                new_bottom = max(all_ys)

                previous["poly"] = [
                    [new_left, new_top],
                    [new_right, new_top],
                    [new_right, new_bottom],
                    [new_left, new_bottom]
                ]

                # Update calculated coordinates
                previous["left_x"] = new_left
                previous["right_x"] = new_right
                previous["center"] = (
                    new_top + new_bottom
                ) / 2
                previous["height"] = new_bottom - new_top

                # Update confidence
                previous["score"] = (
                    previous["score"] + item["score"]
                ) / 2

                matched = True
                break

        if not matched:

            new_item = item.copy()
            new_item["_line_index"] = line_index
            new_item["_column_left_x"] = left_x

            merged_items.append(new_item)

    # Rebuild the lines
    result = {}

    for item in merged_items:

        line_index = item.pop("_line_index")
        item.pop("_column_left_x")

        result.setdefault(line_index, []).append(item)

    return [
        result[index]
        for index in sorted(result)
    ]
