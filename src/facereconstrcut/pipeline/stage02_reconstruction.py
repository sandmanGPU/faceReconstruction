import os, sys
from options.test_options import TestOptions
import torch
import cv2
from src.facereconstrcut.components.reconstruction import ReconstrcutionModel
opt = TestOptions().parse()


STAGE_NAME = 'Reconstruction'
filename = 'pic.jpg'
img = cv2.cvtColor(cv2.imread(filename), cv2.COLOR_BGR2RGB)

if __name__ =='__main__':

    try:
        logger.info(f">>>>>>> stage {STAGE_NAME} started <<<<<<<")
        obj = ReconstrcutionModel(opt)
        visual = obj.reconstruct(img, lm)
        logger.info(f">>>>>>> stage {STAGE_NAME} completed <<<<<<<")
    except Exception as e:
        logger.exception(e)
        raise e