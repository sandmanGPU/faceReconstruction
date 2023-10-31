import sys
from src.facereconstrcut.components.detect_landmark import LM_MTCNN
from src.facereconstrcut import logger
import cv2 
STAGE_NAME = 'Landmark detection'
filename = 'pic.jpg'
img = cv2.cvtColor(cv2.imread(filename), cv2.COLOR_BGR2RGB)

if __name__ =='__main__':

    try:
        logger.info(f">>>>>>> stage {STAGE_NAME} started <<<<<<<")
        obj = LM_MTCNN()
        obj.getLandmarks(img)
        logger.info(f">>>>>>> stage {STAGE_NAME} completed <<<<<<<")
    except Exception as e:
        logger.exception(e)
        raise e



