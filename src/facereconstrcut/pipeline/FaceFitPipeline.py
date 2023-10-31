import os
from src.facereconstrcut.components.detect_landmark import LM_MTCNN
from src.facereconstrcut import logger
import cv2 
from options.test_options import TestOptions
from src.facereconstrcut.components.reconstruction import ReconstrcutionModel
import numpy as np
from util.util import tensor2im, save_image



class FaceFitter():
    def __init__(self, filename):
        self.filename=filename
        self.opt = TestOptions().parse()

    def fitface(self, save_dir):
        self.img = cv2.cvtColor(cv2.imread(self.filename), cv2.COLOR_BGR2RGB)
        obj0 = LM_MTCNN()
        obj1 = ReconstrcutionModel(self.opt)
        lms = obj0.getLandmarks(self.img)
        visuals =[]
        
        j=0
        for entry in lms:
            
            box = entry['box']
            confidence = entry['confidence']
            keypoints = entry['keypoints']
            if confidence < 0.7:
                continue
            lm = np.array(list(keypoints.values()))
            cropped = self.img[box[1]:box[1]+box[3], box[0]:box[0]+box[2]]
            save_image(cropped, os.path.join(save_dir,str(j)+'-detected-cropped.png'))
           
      
            savename=os.path.join(save_dir, str(j)+'.obj')
            visual = obj1.reconstruct(self.img, lm, savename)
            visuals.append(visual)
            for label,image in visual.items():
                print(image.shape)
                for i in range(image.shape[0]):
                    image_numpy = tensor2im(image[i])
                    save_image(image_numpy, os.path.join(save_dir,str(j)+'.png'))
            j = j+1
        return visuals