import logging
import cv2
import numpy as np

logger = logging.getLogger(__name__)
def run_me():
    logger.info(f"Click on the image and your click will be printed!")

    def click_event(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            click_location = (x,y)
            print(click_location)
            annotated_image = image.copy()
            cv2.circle(annotated_image,click_location, 100, (0,0,255), 5)
            cv2.imshow("click to draw a circle", annotated_image)

    image = cv2.imread("/Users/philipqueen/Downloads/standing_pose.JPG")
    cv2.imshow("click to draw a circle", image)

    cv2.setMouseCallback("click to draw a circle", click_event)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_me()
