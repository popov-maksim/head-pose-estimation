"""
Starting point of the app
"""


import argparse
import os
from streaming import *
from pose_estimation import *
from utils import resize


def app(stream: VideoStream, height: int = 480) -> None:
    # initializing
    estimator = PoseEstimator()

    # starting stream
    video = stream.start()
    time.sleep(2)

    is_webcam = isinstance(stream, WebcamVideoStream)

    while True:
        # main loop
        frame = video.read()
        frame = resize(frame, height=height)
        try:
            frame = estimator.estimate_pose(frame)
        except NoDetectedFaces:
            pass
        if is_webcam:
            frame = cv2.flip(frame, 1)  # let's make our camera mirrored
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q") or not video.running():
            cv2.destroyAllWindows()
            video.stop()
            break


def get_stream(arg: tp.Optional[str]) -> tp.Optional[VideoStream]:
    if arg is None:
        # by default there will be used webcam source
        return WebcamVideoStream()

    if arg.lower() == "web":
        return WebcamVideoStream()
    elif os.path.exists(arg):
        return FileVideoStream(arg)

    return None


if __name__ == '__main__':
    # parsing of params
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-s", "--source", required=False, help="'path to video' or 'web'")
    args = arg_parser.parse_args()

    stream = get_stream(args.source)
    if stream is not None:
        app(stream)
    else:
        print("[ERROR] Wrong source for streaming from")
