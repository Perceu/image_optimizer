from PIL import Image
import os 
CURRENT_DIRECTORY = os.getcwd()

img = Image.open(CURRENT_DIRECTORY+'/0_img_original.jpg')
img2 = Image.open(CURRENT_DIRECTORY+'/0_img2.jpg')
img.save('1_0clean_meta_info.jpg')
img.save('2_0optimized.jpg', optimize=True)
img.save('3_0qualit_85.jpg', optimize=True, quality=65)

img2.save('1_1clean_meta_info.jpg')
img2.save('2_1optimized.jpg', optimize=True)
img2.save('3_1qualit_85.jpg', optimize=True, quality=65)