import numpy as np
import cv2
import dlib
import typing as tp


class NoDetectedFaces(Exception):
    """
    Exception for the case when there was no detected faces
    """
    pass


class PoseEstimator:
    """
    Class implements algorithm of pose estimation of a person face
    Usage: initialize an object of the class and use obj.estimate_pose(img) method
    """

    def __init__(self, shape_predictor_path: str = "../model/shape_predictor.dat") -> None:
        self.six_points = [30, 8, 36, 45, 48, 54]
        self.predictor = dlib.shape_predictor(shape_predictor_path)
        self.detector = dlib.get_frontal_face_detector()
        self.dist_coeffs = np.zeros((4, 1))  # assuming no radial distortion
        self.model_points = np.array([
            [0, 0, 0],              # Nose tip
            [0, -330, -65],         # Chin
            [-225, 170, -135],      # Left eye left corner
            [225, 170, -135],       # Right eye right corner
            [-150, -150, -125],     # Left Mouth corner
            [150, -150, -125]       # Right mouth corner
        ], dtype=float)

    def facial_landmark(self, img: np.ndarray) -> np.ndarray:
        """
        Function for computing six points on face:
            left eye left corner,
            right eye right corner,
            left mouth corner,
            right mouth corner,
            nose tip,
            chin

        :param img: image where to find facial six points
        :return: array with coordinates of six points if face is located, raises NoDetectedFaces exception otherwise
        """
        n = 68  # number of landmark points
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # convert to grayscale
        rects = self.detector(gray, 0)

        for (i, rect) in enumerate(rects):
            shape = self.predictor(gray, rect)
            shape = np.array([[shape.part(i).x, shape.part(i).y] for i in range(n)])
            return np.array(shape[self.six_points], dtype=float)

        if len(rects) == 0:
            raise NoDetectedFaces

    def estimate_pose(self, img: np.ndarray) -> tp.Optional[np.ndarray]:
        """
        Estimates person's face pose on given image

        :param img: image to locate face and estimate its pose
        :return: array with six points and pointing line from nose point if face was located,
                 raises NoDetectedFaces in case there was no located face,
                 None in case pose wasn't found
        """
        try:
            image_points = self.facial_landmark(img)
            model_points = self.model_points

            for (x, y) in image_points.astype(int):
                cv2.circle(img, (x, y), 3, (0, 0, 255), -1)

            focal_length = img.shape[1]
            center = (img.shape[1] / 2, img.shape[0] / 2)
            camera_matrix = np.array([[focal_length, 0, center[0]], [0, focal_length, center[1]], [0, 0, 1]],
                                     dtype=float)

            dist_coeffs = self.dist_coeffs
            (success, rotation_vector, translation_vector) = cv2.solvePnP(model_points, image_points, camera_matrix,
                                                                          dist_coeffs)
            if not success:
                print("solvePnP didn't solve system")
                return

            (nose_end_point2D, jacobian) = cv2.projectPoints(np.array([(0.0, 0.0, 1000.0)]), rotation_vector,
                                                             translation_vector, camera_matrix, dist_coeffs)
            p1 = (int(image_points[0][0]), int(image_points[0][1]))
            p2 = (int(nose_end_point2D[0][0][0]), int(nose_end_point2D[0][0][1]))

            return cv2.line(img, p1, p2, (0, 255, 0), 2)
        except NoDetectedFaces:
            raise
