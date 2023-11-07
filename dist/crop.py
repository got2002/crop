# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


#import seaborn as sb
#from flask import Flask
#app = Flask(__name__)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    from PIL import Image
    #img = Image.open("C:\\Users\\kingt\\OneDrive\\Desktop\\DOPA2.2\\84f3bff04d870c7fda2930892b173dd5.jpg")
    img = Image.open("C:\\Users\\gohvf\\Downloads\\Cartiage Case\\Bullet\\Example.jpeg")

    width, height = img.size
   
    img_1_area = (width*0.11, 0, width*0.38, height//2)
    img_2_area = (width*0.48, 0, width*0.76, height//2)
    img_3_area = (width*0.11, height//2, width*0.38, 0)
    img_4_area = (width*0.48, height//2, width*0.76, 0)

    
    img_1 = img.crop(img_1_area)
    img_2 = img.crop(img_2_area)
    img_3 = img.crop(img_3_area)
    img_4 = img.crop(img_4_area)


    img_1.show()
    img_2.show()
    img_3.show()
    img_4.show()
    img_1.save(" C:\\Users\\gohvf\\OneDrive\\เดสก์ท็อป\\GUN\\output_image.jpg")

    exit()