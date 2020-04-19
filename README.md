# Head pose estimation
This repo contains implementation of an algorithm for head pose estimation of a person on a given video.
There was used this [guide](https://www.learnopencv.com/head-pose-estimation-using-opencv-and-dlib/) describing how to implement head pose estimation from a given image.
It was made to work on video.

## Requirements
- The source of video could be a file or a stream from a web camera.
- Information to be displayed on each frame of the resulting video: source frame, 5 landmark points of a face, a ray pointing from a person’s nose
- You can use OpenCV, Dlib and whatever you find useful
- Minimum resolution of a video: 480p.
- There should be one person on a video. Height of a person’s face should be at least 1/3 of the height of the video in terms of pixels.


