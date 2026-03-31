## Problem

I have many digital pics to cull through.  Awhile back I moved most from old flash drives to this old computer and now I need to decide which are worth keeping, so that I can migrate them to perhaps a fire safe, private cloud location.


## Goals?
1. How should I decide which are worth keeping?  What's my reward algorithm?
1. Could I tag these photos by time, location, person name?  Should I cluster by these features?  Should I take a network, neighbor approach to separate the memorable from mundane?
1. Could I identify and remove any duplicates?

## Steps
1. [profile](https://github.com/mondayn/photo-organizer/blob/main/1-profile.ipynb).  Exploration.  How many pics are there?  What can I derive easily?  Extracted file and image metadata.  
1. [dedupe](https://github.com/mondayn/photo-organizer/blob/main/2-dedupe.ipynb) Can i identify duplicates?  I find several GB of photos taken within minutes of each other with similar encodings.  Should I take the first of these dupes or find a way to score them?
1. [faces](https://github.com/mondayn/photo-organizer/blob/main/3-faces.ipynb) Similar to Apple photos, can I tag certain people in my photos? For privacy, I'll determine faces locally using [dlib](https://dlib.net/face_recognition.py.html).  I'm on an old CPU, so I'll use its gradient histogram, SVM algorithm instead of its CNN GPU approach.
1. test, evaluate

## Lessons
1. Sharpening, denoising or greyscale didn't improve face detection.
1. facial rec wasn't good with library skimage.  
1. I find dlib does a better job detecting faces for opencv instead of PIL images.
1. I find reducing image size provides a speedup without noticable accuracy loss.


## Outcome

1. 

## ToDo
1. can i move pics to thumbdrive, to newer computer
1. multi thread dlib?
1. https://github.com/openai/CLIP - for saliency?
1. how many have geo lat and what are those locations?  are they important?
1. perceptual hash - could i use to network similar pics?
1. decide which of 1:many dupes to keep.  prefer larger or second?
1.  ~~can i improve quality similar to pix to improve facial rec?~~
1. find examples of pics not important
1. dedupe: use sharpness, colorfulness, contrast, saliency scores to break ties?

-   /mnt/4C74F47B74F468DA/Pictures/IMG_0822-2005-01-04 015604.JPG -- blurry finger 
-   /mnt/4C74F47B74F468DA/Pictures/IMG_0823-2005-01-04 015606.JPG -- blurry red nothing
