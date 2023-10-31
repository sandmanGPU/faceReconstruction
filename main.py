import sys, os
from src.facereconstrcut.components.detect_landmark import LM_MTCNN
from src.facereconstrcut import logger
from src.facereconstrcut.utils.common import save_json
import cv2 
from options.test_options import TestOptions
from src.facereconstrcut.components.reconstruction import ReconstrcutionModel
import numpy as np
from util.util import tensor2im, save_image
opt = TestOptions().parse()
filename = 'artifacts/pic3.jpg'
img = cv2.cvtColor(cv2.imread(filename), cv2.COLOR_BGR2RGB)
detect_dir = './logs/detections/'
from src.facereconstrcut.pipeline.FaceFitPipeline import FaceFitter
os.makedirs(detect_dir, exist_ok=True)

# STAGE_NAME = 'Landmark detection'
# try:
#     logger.info(f">>>>>>> stage {STAGE_NAME} started <<<<<<<")
#     obj = LM_MTCNN()
#     lms = obj.getLandmarks(img)
#     json_savename = (os.path.join(detect_dir, os.path.splitext(filename)[0])+'.json')
#     save_json(json_savename, lms)
#     lm = lms[0]
#     face_entry = lms[0]
#     keypoints =  face_entry['keypoints']
#     lm = np.array(list(keypoints.values()))
#     print(lm)

   
#     logger.info(f">>>>>>> stage {STAGE_NAME} completed <<<<<<<")
# except Exception as e:
#     logger.exception(e)
#     raise e


# STAGE_NAME = 'Reconstruction'

# try:
#     logger.info(f">>>>>>> stage {STAGE_NAME} started <<<<<<<")
#     obj = ReconstrcutionModel(opt)
#     visual = obj.reconstruct(img, lm)

#     for label,image in visual.items():
#         for i in range(image.shape[0]):
#                 image_numpy = tensor2im(image[i])

#                 save_image(image_numpy, 'image.png')
#     logger.info(f">>>>>>> stage {STAGE_NAME} completed <<<<<<<")
# except Exception as e:
#     logger.exception(e)
#     raise e

ff = FaceFitter(filename)
visuals = ff.fitface('./artifacts/')
