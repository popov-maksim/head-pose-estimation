import time
import cv2
import numpy as np
import typing as tp
from threading import Thread
from queue import Queue
from abc import abstractmethod


class VideoStream:
    """
    Abstract class fro video streaming
    """
    def __init__(self, src: tp.Union[str, int], name: str) -> None:
        self.stream = cv2.VideoCapture(src)
        self.name: str = name
        self.stopped: bool = False
        self.thread = Thread(target=self.update, name=self.name, args=())
        self.thread.daemon = True

    @abstractmethod
    def start(self) -> "VideoStream":
        pass

    @abstractmethod
    def update(self) -> None:
        pass

    @abstractmethod
    def read(self) -> np.ndarray:
        pass

    @abstractmethod
    def stop(self) -> None:
        pass

    @abstractmethod
    def running(self) -> bool:
        pass


class WebcamVideoStream(VideoStream):
    def __init__(self, src: tp.Union[str, int] = 0, name: str = "WebcamVideoStream") -> None:
        super().__init__(src, name)
        _, self.frame = self.stream.read()

    def start(self) -> VideoStream:
        self.thread.start()
        return self

    def update(self) -> None:
        while True:
            if self.stopped:
                return
            _, self.frame = self.stream.read()

    def read(self) -> np.ndarray:
        return self.frame

    def running(self) -> bool:
        return not self.stopped

    def stop(self) -> None:
        self.stopped = True
        self.stream.release()


class FileVideoStream(VideoStream):
    def __init__(self, src: tp.Union[str, int], name="VideoFile", queue_size=128) -> None:
        super().__init__(src, name)
        self.frames_queue = Queue(maxsize=queue_size)

    def start(self) -> VideoStream:
        self.thread.start()
        return self

    def update(self) -> None:
        while not self.stopped:
            if not self.frames_queue.full():
                is_grabbed, frame = self.stream.read()
                if not is_grabbed:
                    self.stopped = True
                else:
                    self.frames_queue.put(frame)
            else:
                time.sleep(0.1)  # Rest for 10ms, we have a full queue

    def read(self) -> np.ndarray:
        return self.frames_queue.get()

    def running(self) -> bool:
        return self.more() or not self.stopped

    def more(self) -> bool:
        tries = 0
        while self.frames_queue.qsize() == 0 and not self.stopped and tries < 5:
            time.sleep(0.1)
            tries += 1
        return self.frames_queue.qsize() > 0

    def stop(self) -> None:
        self.stopped = True
        self.stream.release()
        self.thread.join()
