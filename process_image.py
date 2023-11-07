from PIL import Image
import sys
import os
import psycopg2
import pandas as pd
from pathlib import Path
import logging  
from datetime import datetime
#input_path = "C:\\Users\\gohvf\\Downloads\\Cartiage Case\\Bullet\\"

line_cases_start = 2
line_cases_end = 6
line_bullet_start = 8
line_bullet_end = 12
line_db = 14


def crop_and_save_images_from_db(input_cases,input_bullet,output_dir):
    try:

        config_file_path = Path("./config.txt")
        with config_file_path.open('r', encoding='utf-8') as crop_file:
            lines = crop_file.readlines()

            scale_crop_cases = [tuple(map(float, line.strip().split(','))) for line in lines[line_cases_start:line_cases_end]]
            scale_crop_bullet = [tuple(map(float, line.strip().split(','))) for line in lines[line_bullet_start:line_bullet_end]]
            DB_param = tuple(lines[line_db].split(','))
        #print(DB_param)
        
        conn = psycopg2.connect(database=DB_param[0].strip(),
                                host=DB_param[1].strip(),
                                user=DB_param[2].strip(),
                                password=DB_param[3].strip(),
                                port=DB_param[4].strip())
        
        cursor = conn.cursor()


        cmd_ex = "Select * from \"View_jpgCases\""
        cursor.execute(cmd_ex)

        rows = cursor.fetchall()
        

        
        for i, row in enumerate(rows):
            #image_path = input_bullet +  f"{row[1]}.jpeg"
            image_path= os.path.join(input_cases, f"{row[1]}.jpeg")
            img = Image.open(image_path)
            width, height = img.size

            os.makedirs(output_dir, exist_ok=True)

            # Crop and save each section for folder 1 Cases
            for j, crop_coords in enumerate(scale_crop_cases):
                crop_coords = tuple(int(val * width if idx % 2 == 0 else val * height) for idx, val in enumerate(crop_coords))
                cropped_img = img.crop(crop_coords)
                output_image_path = os.path.join(output_dir, f"{row[0]}_{j + 1}.jpg")
                
                if not cropped_img.getbbox():
                    print(f"Skipping empty crop: {output_image_path}")
                else:
                    cropped_img.save(output_image_path)
                   # print(f"Cropped image {i + 1}_{j + 1} saved to {output_image_path}")

        # cases finish

        
        #bullet start
        cmd_ex = "Select * from \"View_jpgBullet\""
        cursor.execute(cmd_ex)

        rows = cursor.fetchall()
        
        for i, row in enumerate(rows):
            image_path = row[1] + ".jpeg"
            image_path= os.path.join(input_bullet, f"{row[1]}.jpeg")
            img = Image.open(image_path)
            width, height = img.size

            os.makedirs(output_dir, exist_ok=True)

            # Crop and save each section for folder 2 Bullet 
            for j, crop_coords in enumerate(scale_crop_bullet):
                crop_coords = tuple(int(val * width if idx % 2 == 0 else val * height) for idx, val in enumerate(crop_coords))
                cropped_img = img.crop(crop_coords).rotate(90, expand=True)
                output_image_path = os.path.join(output_dir, f"{row[0]}_{j + 1}.jpg")
                if not cropped_img.getbbox():
                    print(f"Skipping empty crop: {output_image_path}")
                else:
                    cropped_img.save(output_image_path)
                   # print(f"Cropped image {i + 1}_{j + 1} saved to {output_image_path}")

        #bullet finish            
        conn.close()
    except Exception as e:
        logging.error(f"Error: {e}")
        print(f"Error: {e}")
        
    
if __name__ == "__main__":
    
    if len(sys.argv) != 4:
        error_message = "Error: Invalid number of arguments. input_directory_cases input_directory_bullet output_directory"
        print(error_message)
        
        sys.exit(1)
    
    input_cases = sys.argv[1]   
    input_bullet = sys.argv[2]
    output_dir = sys.argv[3]

    
  
    crop_and_save_images_from_db(input_cases, input_bullet, output_dir)



