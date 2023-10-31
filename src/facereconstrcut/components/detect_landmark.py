#will be using mtcnn for 5x2 landmarks

import os
from mtcnn import MTCNN

class LM_MTCNN:
    def __init__(self):
        self.detector = MTCNN()

    def getLandmarks(self, image):
        lm_details = self.detector.detect_faces(image)
        return lm_details