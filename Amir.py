import pandas as pd
import ast
import os
import shutil
import numpy as np
from sklearn import model_selection
from tqdm import tqdm





#from fstrings import f 

Data_path="/home/amir/Downloads/global wheat/global-wheat-detection (1)" 

Output_path="/home/amir/Downloads/y5/yolov5-master/wheat_data/"

def process_data(data,data_type="train"):
    for _, row in tqdm(data.iterrows(),total=len(data)): 
         image_name=row["image_id"]
         bounding_boxes=row["bboxes"]
         yolo_data=[]
         for bbox in bounding_boxes:
             x=bbox[0]
             y=bbox[1]
             w=bbox[2]
             h=bbox[3]
             x_center=x+w/2
             y_center=y+h/2
             x_center/=1024.0
             y_center/=1024.0
             w/=1024.0
             h/=1024.0
             yolo_data.append([0,x_center,y_center,w,h])
         yolo_data=np.array(yolo_data)
         np.savetxt(os.path.join(Output_path, f"labels/{data_type}/{image_name}.txt"),yolo_data,fmt=["%d","%f","%f","%f","%f"])
        
         shutil.copyfile(os.path.join(Data_path,f"train/{image_name}.jpg"),os.path.join(Output_path,f"images/{data_type}/{image_name}.jpg"))

if __name__ == "__main__":
    df=pd.read_csv(os.path.join(Data_path,"train.csv"))
    df.bbox=df.bbox.apply(ast.literal_eval)
    df=df.groupby("image_id")["bbox"].apply(list).reset_index(name="bboxes")
    
    df_train,df_valid=model_selection.train_test_split(df,test_size=0.1,random_state=42,shuffle=True)
    df_train=df_train.reset_index(drop=True)
    df_valid=df_valid.reset_index(drop=True)
    process_data(df_train,data_type="train")
    process_data(df_valid,data_type="validation")
