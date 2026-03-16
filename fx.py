#region imports
from pathlib import Path
from toolz import thread_first, pipe
import os
import numpy as np
import pandas as pd
import datetime
#import janitor

import PIL
from PIL import ExifTags
from functools import lru_cache

import cv2

from IPython.display import Image, display
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"

from face_recognition import (
    load_image_file, 
    face_encodings,
    compare_faces
)


#endregion imports

#region munging
def add_col(self,**kwargs):
    ''' assign new columns using itertuples, e.g. 
        df.add_col(
            new_col=lambda x: 'y' if 'F' in x.state_code else 'N'
            ,new_col2=lambda x: 'y' if 'G' in x.state_code else 'N'
        )
     '''
    _df = self.copy()
    for k, v in kwargs.items():
        _df[k] = list(map(v,_df.itertuples()))
    return _df

def print_cols(df): 
    print(list(df.columns))
    return df

def print_shape(df):
    print(df.shape)
    return df

def get_dupes(df,column_names): 
    return df.loc[df.duplicated(subset=column_names, keep=False)]

for fx in [ add_col, print_cols, get_dupes, print_shape ]:
    setattr(pd.DataFrame, fx.__name__, fx)
#endregion munging


#region image metadata (exif)

# def ignore_exceptions(func):
#     def wrapper(*args, **kwargs):
#         try:
#             return func(*args, **kwargs)
#         except Exception as e:
#             print(f"Error in {func.__name__}: {e}")
#             return None
#     return wrapper

@lru_cache
def get_exif(file):
    ''' extract metadata from img

    for k,v in PIL.ExifTags.TAGS.items():
        if 'Date' in v:
            print(k,v)
        if 'GPSInfo' in v:
            print(k,v)
            
    for i,j in enumerate(PIL.ExifTags.GPSTAGS.items()):
        if i>6: break
        print(j[0],j[1])
    '''
    dt, lat, lng = None, None, None
    try:
        exif = PIL.Image.open(file)._getexif()
        dt = datetime.datetime.strptime(
            exif[36867], #DateTimeOriginal 
            "%Y:%m:%d %H:%M:%S")

        latref=exif[34853][1]
        lat=exif[34853][2]
        lngref=exif[34853][3]
        lng=exif[34853][4]

        def dms_to_decimal(deg, minutes, seconds, direction):
            dec = deg + minutes/60 + seconds/3600
            if direction in ['S', 'W']:
                dec = -dec
            return float(dec)
        lat = dms_to_decimal(lat[0],lat[1],lat[2],exif[34853][1]) 
        lng = dms_to_decimal(lng[0],lng[1],lng[2],exif[34853][3])
    except Exception as e:
        pass
    
    return dt,lat,lng
#endregion image metadata


#region faces
def get_encodings(path):
    try:
        return pipe(path,load_image_file,face_encodings)
    except:
        return []

def show(image):
    display(Image(image, width=100,))

def save_encodings(path,encodings):
    np.savez_compressed(path,encodings)

def load_encodings(path):
    data = np.load(path)
    return [data[f'arr_{i}'] for i in range(len(data.files))]
#endregion faces


#region dedupe with opencv

def hist(path):
    img = cv2.imread(path)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hue_saturation=[0,1]
    bins=[50,60]
    ranges=[0,180,0,256]
    return cv2.calcHist([hsv],hue_saturation,None,bins,ranges)

#endregion dedupe with opencv


if __name__=='__main__':
    file= '/mnt/4C74F47B74F468DA/Pictures/DSC_0024-2015-05-06 221910.JPG'
    # file ='/mnt/4C74F47B74F468DA/Pictures/IMG_1458-2016-12-18 025702.JPG'  # should have lat long
    # file='/mnt/4C74F47B74F468DA/Pictures/BORE1037-2018-10-11 001716.JPG' #africa
    # file='/mnt/4C74F47B74F468DA/DCIM/201904__/IMG_0991.JPG'
    # file='/mnt/4C74F47B74F468DA/Pictures/n iphone/2022-01-07 001/Internal Storage/DCIM/101APPLE/IMG_1015.JPG'

    thread_first(
        file,
        get_exif,
        print
    )


