import cv2
import numpy as np


def process_frame(frame, templates, threshold):
    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    for template in templates:
        result = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(result >= threshold)

        if loc[0].size > 0:
            # Get the coordinates of the first match
            pt = (loc[1][0], loc[0][0])

            # Draw a rectangle around the match
            cv2.rectangle(
                frame, pt, (pt[0] + template.shape[1], pt[1] + template.shape[0]), (0, 0, 255), 2)

            cv2.putText(frame, 'Object', (pt[0], pt[1]-6), cv2.FONT_HERSHEY_PLAIN,
                        2, (0, 0, 255), 2, cv2.LINE_AA)

            break  # try with more than one object

    return frame
