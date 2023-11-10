import os 
from options.test_options import TestOptions
from models import create_model
import torch
from scipy.io import loadmat, savemat
from util.load_mats import load_lm3d
from util.preprocess import align_img
from PIL import Image
import numpy as np
class ReconstrcutionModel:
    def __init__(self, opt, rank=0):
        device = torch.device(rank)
        torch.cuda.set_device(device)
        self.model = create_model(opt)
        self.model.setup(opt)
        self.model.device=device
        self.model.parallelize()
        self.model.eval()
        self.lm3d_std = load_lm3d(opt.bfm_folder)

    def align_to_lm(self, img, lm, to_tensor=True):
        # to RGB 
        img = Image.fromarray(img)
        W,H = img.size
        _, im, lm, _ = align_img(img, lm, self.lm3d_std)
        if to_tensor:
            im = torch.tensor(np.array(im)/255., dtype=torch.float32).permute(2, 0, 1).unsqueeze(0)
            lm = torch.tensor(lm).unsqueeze(0)
        return im, lm



    def reconstruct(self, img, lm, savename):
        im_tensor, lm_tensor = self.align_to_lm(img, lm)
        data = {
            'imgs': im_tensor,
            'lms': lm_tensor
        }
        self.model.set_input(data)
        self.model.test() 
        # visuals = self.model.get_current_visuals()  # get image results
       

        self.model.save_mesh(savename) # save reconstruction meshes
        # self.model.save_coeff(os.path.join(save_dir,'face.obj')) # save predicted coefficients

        # return visuals

if __name__ == "__main__":
    print("Running Facefitter\n")