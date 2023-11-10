import os
from src.facereconstrcut.components.detect_landmark import LM_MTCNN
from src.facereconstrcut import logger
import cv2 
from options.test_options import TestOptions
from src.facereconstrcut.components.reconstruction import ReconstrcutionModel
import numpy as np
from util.util import tensor2im, save_image
import base64


class FaceFitter():
    def __init__(self, filename):
        self.filename=filename
        self.opt = TestOptions().parse()

    def fitface(self, save_dir):
        # logger.info("Now loading file: ", self.filename)
        self.img = cv2.cvtColor(cv2.imread(self.filename), cv2.COLOR_BGR2RGB)
        obj0 = LM_MTCNN()
        obj1 = ReconstrcutionModel(self.opt)
        lms = obj0.getLandmarks(self.img)
        visuals =[]
        obj_list = [] #list to hold saved obj files
        crop_list = [] #list  to hold saved cropped images
        base64_crops = []
        j=0
        save_prefix = os.path.basename(self.filename).split('.')[0]
        for entry in lms:
            
            box = entry['box']
            confidence = entry['confidence']
            keypoints = entry['keypoints']
            if confidence < 0.9 or (box[2] < 200) or (box[3] < 200):
                continue
            lm = np.array(list(keypoints.values()))
            cropped = self.img[box[1]:box[1]+box[3], box[0]:box[0]+box[2]]
            _, buffer = cv2.imencode(".png", cropped)  # Convert to PNG image
            # base64_image = base64.b64encode(buffer).decode("utf-8")
            # base64_crops.append(base64_image)
            crop_savename = os.path.join(save_dir,save_prefix+'-'+str(j)+'-crop.jpg')
            save_image(cropped, crop_savename)
            crop_list.append(save_prefix+'-'+str(j)+'-crop.jpg')
      
            obj_savename=os.path.join(save_dir, save_prefix+'-'+str(j)+'.obj')
            # visual = obj1.reconstruct(self.img, lm, obj_savename)
            obj_list.append(save_prefix+'-'+str(j)+'.obj')
            # visuals.append(visual)
            # for label,image in visual.items():
            #     print(image.shape)
            #     for i in range(image.shape[0]):
            #         image_numpy = tensor2im(image[i])
                  
            #         save_image(image_numpy, os.path.join(save_dir,str(j)+'.png'))
            j = j+1
        return obj_list, crop_list