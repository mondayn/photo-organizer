## Problem

I have many digital pics to cull through.  Awhile back I moved most from old flash drives to this old computer and now I need to decide which are worth keeping, so that I can migrate them to perhaps a fire safe, private cloud location.


## Goals?
1. How should I decide which are worth keeping?  What's my reward algorithm?
1. Could I tag these photos by time, location, person name?  Should I cluster by these features?  Should I take a network, neighbor approach to separate the memorable from mundane?
1. Could I identify and remove any duplicates?

## Steps
1. [profile](https://github.com/mondayn/photo-organizer/blob/main/1-profile.ipynb).  Exploration.  How many pics are there?  What can I derive easily?  Extracted file and image metadata.  
1. [dedupe](https://github.com/mondayn/photo-organizer/blob/main/2-dedupe.ipynb) Can i identify duplicates or pics taken quickly together?  Looks like I can reduce several GB.
1. [face preprocess](https://github.com/mondayn/photo-organizer/blob/main/3-face_preprocess.ipynb) Similar Apple photos, can I tag certain people in my photos? For privacy, I'll determine faces locally using dlib, and this old computer means I can't use GPU or its CNN model :( dlib does a good job finding faces, but I came across a couple of examples where it did not detect faces and after opening these in pix and saving with enhanced quality, dlib detects their faces.  So I'll test enhancing to improve recognition and see if reducing pic size reduces processing time without sacrificing accurancy.
1. [labeling](https://github.com/mondayn/photo-organizer/blob/main/4-labeling.ipynb) Curate a few faces to recognize among my entire set.
1. test, evaluate


## Lessons
1. pix 'save as' enhanced helps dlib facial recognition
1. facial rec wasn't good with skimage.  


## Outcome

1. 

## ToDo
1. should i reduce image size for speed?  is facial rec worse for smaller?
1. is facial rec better for color or greyscale
1. multi thread dlib?
1. how many have geo lat and what are those locations?  are they important?
1. perceptual hash - could i use to network similar pics?
1. decide which of 1:many dupes to keep.  prefer larger or second?
1.  ~~can i improve quality similar to pix to improve facial rec?~~
1. find examples of pics not important

-   /mnt/4C74F47B74F468DA/Pictures/IMG_0822-2005-01-04 015604.JPG -- blurry finger 
-   /mnt/4C74F47B74F468DA/Pictures/IMG_0823-2005-01-04 015606.JPG -- blurry red nothing




