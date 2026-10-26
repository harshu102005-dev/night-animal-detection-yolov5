import cv2
import numpy as np

def enhance(image_rgb):
    lab = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2LAB)
    l,a,b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8,8))
    cl = clahe.apply(l)
    lab = cv2.merge((cl,a,b))
    rgb = cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)

    gamma = 1.4
    corrected = np.power(rgb/255.0, gamma)*255
    corrected = np.clip(corrected,0,255).astype(np.uint8)
    return corrected