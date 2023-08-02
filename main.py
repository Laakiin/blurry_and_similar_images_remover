import PIL
from sewar.full_ref import uqi
from PIL import Image
import os
import numpy as np
import cv2

#funtion that list all the images in the current directory handling caps, it will ignore all the other files
#and return a list of all the images
def list_img():
    imgs = []
    for file in os.listdir():
        if file.endswith(".jpg") or file.endswith(".png") or file.endswith(".jpeg") or file.endswith(".JPG") or file.endswith(".JPEG") or file.endswith(".PNG"):
            imgs.append(file)
        else:
            continue
    return imgs

def remove_blurry(imgs,logs_file):
    try:
        rmv=[]
        for i in range(len(imgs)):
            img = np.array(Image.open(imgs[i]))
            laplacian = cv2.Laplacian(img, cv2.CV_64F).var()
            logs_file.write(f"Blurry value of '{imgs[i]}': {laplacian}\n")
            print(f"Blurry value of '{imgs[i]}': {laplacian}")
            if laplacian < 10:
                logs_file.write(f"{imgs[i]} is too blurry and has been deleted\n")
                print(f"{imgs[i]} is too blurry and has been deleted")
                rmv.append(imgs[i])
                os.remove(imgs[i])
                imgs.remove(imgs[i])
            else:
                continue
        return imgs, rmv
    except IndexError:
        return imgs, rmv
    except PIL.UnidentifiedImageError:
        logs_file.write("PIL.UnidentifiedImageError\n")
        imgs.remove(imgs[i])
        remove_blurry(imgs,logs_file)
        return imgs, rmv
    except PermissionError:
        logs_file.write("PermissionError\n")
        remove_blurry(imgs,logs_file)
        return imgs, rmv

def remove_double(imgs,logs_file):
    try:
        rmv=[]
        for i in range(len(imgs)):
            for j in range(len(imgs)):
                if i != j:
                    img1 = np.array(Image.open(imgs[i]))
                    img2 = np.array(Image.open(imgs[j]))
                    if img1.shape == img2.shape:
                        uqi_value = uqi(img1, img2)
                        logs_file.write(f"Similarity between '{imgs[i]}' and '{imgs[j]}': {round(uqi_value*100,2)}%\n")
                        print(f"Similarity between '{imgs[i]}' and '{imgs[j]}': {round(uqi_value*100,2)}%")
                        if uqi_value > 0.82:
                            logs_file.write(f"{imgs[i]} is similar to {imgs[j]} and has been deleted\n")
                            print(f"{imgs[i]} is similar to {imgs[j]} and has been deleted")
                            rmv.append(imgs[i])
                            os.remove(imgs[i])
                            imgs.remove(imgs[i])
                            break
                        else:
                            continue
                    else:
                        continue
                else:
                    continue
        return imgs,rmv
    except IndexError:
        return imgs,rmv
    except PIL.UnidentifiedImageError:
        logs_file.write("PIL.UnidentifiedImageError\n")
        imgs.remove(imgs[i])
        remove_double(imgs)
        return imgs,rmv
    except PermissionError:
        logs_file.write("PermissionError\n")
        remove_double(imgs)
        return imgs,rmv

if __name__ == '__main__':
    imgs = list_img()
    logs_file= open("logs.txt", "a")
    logs_file.write(f"------------------------------------\n")
    logs_file.write(f"Images that are going to be analysed: {imgs}\n")
    logs_file.write(f"Number of images: {len(imgs)}\n")
    logs_file.write(f"{os.popen('date /t').read()}{os.popen('time /t').read()}\n")
    logs_file.write("Logs begin:\n")
    blur_removed, rmv = remove_blurry(imgs,logs_file)
    logs_file.write(f"Blurry images removed: \n{rmv}\n")
    double_removed, rmv = remove_double(blur_removed,logs_file)
    logs_file.write(f"Double images removed: \n{rmv}\n")
    logs_file.write("Logs end\n")
    logs_file.write(f"------------------------------------\n")
    logs_file.close()
    print("Program finished")
    os.system("pause")



