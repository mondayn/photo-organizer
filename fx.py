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

for fx in [ add_col ]:
    setattr(pd.DataFrame, fx.__name__, fx)
#endregion munging

#region file & image info

def file_size(file):
    return os.stat(file).st_size

# def ignore_exceptions(func):
#     def wrapper(*args, **kwargs):
#         try:
#             return func(*args, **kwargs)
#         except Exception as e:
#             print(f"Error in {func.__name__}: {e}")
#             return None
#     return wrapper

def get_exif(file):
    try:
        return PIL.Image.open(file)._getexif()
    except:
        pass 

def get_exif_data(file):
    dt = None
    lat = None
    lon = None

    exif_data = {}
    info = get_exif(file)
    if info:
        for tag, value in info.items():
            decoded = ExifTags.TAGS.get(tag, tag)

            if decoded == "DateTimeOriginal":
                dt = value

            if decoded == "GPSInfo":
                gps_data = {}
                for t in value:
                    sub_decoded = ExifTags.GPSTAGS.get(t, t)
                    gps_data[sub_decoded] = value[t]
                exif_data[decoded] = gps_data
            else:
                exif_data[decoded] = value

    if "GPSInfo" in exif_data:		
        gps_info = exif_data["GPSInfo"]

        gps_latitude = gps_info.get('GPSLatitude')
        gps_latitude_ref = gps_info.get('GPSLatitudeRef')
        gps_longitude = gps_info.get('GPSLongitude')
        gps_longitude_ref = gps_info.get('GPSLongitudeRef')

        def to_degrees(value):
            d0 = value[0][0]
            d1 = value[0][1]
            d = float(d0) / float(d1)

            m0 = value[1][0]
            m1 = value[1][1]
            m = float(m0) / float(m1)

            s0 = value[2][0]
            s1 = value[2][1]
            s = float(s0) / float(s1)
            return d + (m / 60.0) + (s / 3600.0)

        if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
            lat = to_degrees(gps_latitude)
            if gps_latitude_ref != "N":                     
                lat = 0 - lat

            lon = to_degrees(gps_longitude)
            if gps_longitude_ref != "E":
                lon = 0 - lon
    return dt, lat, lon

# requires api key
# from urllib.request import urlopen
# import json
# def getplace(lat, lon):
#     url = "http://maps.googleapis.com/maps/api/geocode/json?"
#     url += "latlng=%s,%s&sensor=false" % (lat, lon)
# #     print(url)
#     v = urlopen(url).read()
#     j = json.loads(v)
#     components = j['results'][0]['address_components']
#     country = town = None
#     for c in components:
#         if "country" in c['types']:
#             country = c['long_name']
#         if "postal_town" in c['types']:
#             town = c['long_name']
#     return town, country
# ['results'][1]['formatted_address']

#endregion file & image info

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

if __name__=='__main__':
    file= '/mnt/4C74F47B74F468DA/Pictures/DSC_0024-2015-05-06 221910.JPG'
    # file='/mnt/4C74F47B74F468DA/Pictures/BORE1037-2018-10-11 001716.JPG' #africa
    # file='/mnt/4C74F47B74F468DA/DCIM/201904__/IMG_0991.JPG'
    # file='/mnt/4C74F47B74F468DA/Pictures/n iphone/2022-01-07 001/Internal Storage/DCIM/101APPLE/IMG_1015.JPG'

    thread_first(
        file,
        # get_exif,
        # get_lat_lon,
        get_exif_data,
        # file_size,
        print
    )


