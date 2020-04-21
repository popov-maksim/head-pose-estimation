# Head pose estimation
This repo contains implementation of an algorithm for head pose estimation of a person on a given video.
There was used this [guide](https://www.learnopencv.com/head-pose-estimation-using-opencv-and-dlib/) describing how to implement head pose estimation from a given image.
It was made to work on video. 

# Functionality
- Six points on a frame are determined: left eye left corner, right eye right corner, chin, nose, mouth left and right corners
- Pointing line from nose point is shown (it shows face position regarding the camera)
- Video stream either from webcam or from given video shown on a screen

# Usage
#### Using docker container
Simple way to run the app is to build (takes time) docker image from given Dockerfile or download ready one from DockerHub.
Then just run docker container.

**Command to pull image:** docker pull maxloki/head_pose:ready

**Command to run container with stream from webcam:**
*docker run --device=/dev/video0:/dev/video0 -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=$DISPLAY head_pose:latest*

**Command to run container with stream from video:**
*docker run -v /path/to/videofilename:/videofilename --device=/dev/video0:/dev/video0 -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=$DISPLAY head_pose:latest -s videofilename*

#### Locally from src
Also it is possible to run the app from **src** folder just typing *python main.py* (you need installed opencv and dlib).
It takes one optional parameter *-s [SOURCE]*, give there path to a videofile if you want to use stream from video, don't pass anything if you want stream from webcam.  

#### How to exit
To exit the app just press 'q'
