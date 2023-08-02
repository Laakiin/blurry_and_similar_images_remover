import PIL
from sewar.full_ref import uqi
from PIL import Image
import os
import numpy as np
import cv2


def list_img():
    imgs = []
    for file in os.listdir():
        if file.endswith(".jpg") or file.endswith(".png") or file.endswith(".jpeg") or file.endswith(".JPG") or file.endswith(".JPEG") or file.endswith(".PNG"):
            imgs.append(file)
        else:
            continue
    return imgs

#function that compare 2 images and return the similarity between them without logs
def compare(img1,img2):
    img1 = np.array(Image.open(img1))
    img2 = np.array(Image.open(img2))
    if img1.shape == img2.shape:
        uqi_value = uqi(img1, img2)
        return uqi_value
    else:
        return 0

#function that removes the images that are too blurry
def remove_blurry(imgs,logs_file):
    try:
        for i in range(len(imgs)):
            img = np.array(Image.open(imgs[i]))
            laplacian = cv2.Laplacian(img, cv2.CV_64F).var()
            logs_file.write(f"Blurry value of '{imgs[i]}': {laplacian}\n")
            print(f"Blurry value of '{imgs[i]}': {laplacian}")
            if laplacian < 10:
                logs_file.write(f"{imgs[i]} is too blurry and has been deleted\n")
                print(f"{imgs[i]} is too blurry and has been deleted")
                os.remove(imgs[i])
                imgs.remove(imgs[i])
            else:
                continue
        return imgs
    except IndexError:
        return imgs
    except PIL.UnidentifiedImageError:
        logs_file.write("PIL.UnidentifiedImageError\n")
        imgs.remove(imgs[i])
        remove_blurry(imgs,logs_file)
        return imgs
    except PermissionError:
        logs_file.write("PermissionError\n")
        remove_blurry(imgs,logs_file)
        return imgs



if __name__ == '__main__':
    #imgs variable is an empty list
    imgs = []
    imgs.append("013.jpg")
    imgs.append("014.jpg")
    print(compare(imgs[0],imgs[1]))
    print("Done")
