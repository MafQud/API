import pickle
from pathlib import Path
from typing import Dict, Optional
from urllib.request import Request, urlopen

import cv2
import joblib
import numpy as np
from deepface.detectors.FaceDetector import alignment_procedure
from mtcnn import MTCNN
from sklearn import neighbors
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    f1_score,
    precision_recall_fscore_support,
    precision_score,
    recall_score,
)
from sklearn.preprocessing import Normalizer
from tensorflow.keras.models import load_model


class MafQud:
    def __init__(
        self, facenet_path: Path, knn_path: Path, data: np.ndarray, labels: np.ndarray
    ) -> None:
        self.knn_path = knn_path
        self.detector = MTCNN()
        self.facenet = load_model(facenet_path)
        self.knn = joblib.load(open(knn_path, "rb"))
        self.data = data
        self.labels = labels

    def detect_align_face(self, img: np.ndarray) -> np.ndarray:
        """Detect face with 4 landmarks and align

        Args:
            img (np.ndarray): image array

        Returns:
            numpy.ndarray, list: image array, list of face landmarks and bounding box data
        """
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        detections = self.detector.detect_faces(img)
        if len(detections) == 0 or len(detections) > 1:
            return None

        # Crop and align the face
        x, y, w, h = detections[0]["box"]
        x1, y1 = int(x), int(y)
        x2, y2 = int(x + w), int(y + h)
        face = img[y1:y2, x1:x2]
        keypoints = detections[0]["keypoints"]
        face_align = alignment_procedure(
            face, keypoints["left_eye"], keypoints["right_eye"]
        )

        # resize the face and convert to numpy array
        face_align = cv2.resize(face_align, (160, 160))
        face_array = np.asarray(face_align)

        return face_array

    def feature_encoding(self, img: np.ndarray) -> np.ndarray:
        """Extract 128 numerical feature from face array

        Args:
            img (numpy.ndarray): face array

        Returns:
            numpy.ndarray: array of 128 numerica feature
        """
        img = img.astype("float32")
        mean, std = img.mean(), img.std()
        img = (img - mean) / std
        samples = np.expand_dims(img, axis=0)
        yhat = self.facenet.predict(samples)

        return yhat[0]

    def encode_photo(self, url: str) -> np.ndarray:
        """Extract 128 numerical feature from face array

        Args:
            url (str): url to image

        Returns:
            numpy.ndarray: array of 128 numerical feature
        """
        req = Request(url, headers={"User-Agent": "XYZ/3.0"})
        data = urlopen(req)
        arr = np.asarray(bytearray(data.read()), dtype=np.uint8)
        img = cv2.imdecode(arr, -1)
        face = self.detect_align_face(img)
        if face is None:
            return None

        embedding = self.feature_encoding(face).reshape(1, -1)

        return embedding

    def normalize_images(self, *, kind: Optional[str] = "l2") -> np.ndarray:
        """Normalize training data

        Args:
            kind (str): type of normalization. Defaults to "l2".
        Returns:
            numpy.ndarray: X normalized
        """
        in_encoder = Normalizer(norm=kind)
        X = in_encoder.transform(self.data)
        return X

    def KNN_Classifier(self, n_neighbors: Optional[int] = 3):
        """KNN classifier to classify faces

        Args:
            n_neighbors (int, optional):number of nearest neighbors Defaults to 1.

        Returns:
            sklearn_model: KNN model
        """
        X = self.normalize_images()
        knn_clf = neighbors.KNeighborsClassifier(
            n_neighbors=n_neighbors, algorithm="ball_tree", weights="distance"
        )
        knn_clf.fit(X, self.labels)
        return knn_clf

    def evaluate(self, X_test, y_test):
        """Evaluate model
        Args:
            model (tensorflow.python.keras.engine.functional.Functional): acenet keras model
            X_test (numpy.ndarray): array of all faces for each person
            y_test (numpy.ndarray): array of labels for each face

        Returns:
            accuracy (float): model accuracy
            precision (float): model precision
            recall (float): model recall
            f1 (float): model f1_score"""
        X_test = self.normalize_images(X_test)
        y_pred = self.knn.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, average="weighted", zero_division=0)
        recall = recall_score(y_test, y_pred, average="weighted", zero_division=0)
        f1 = f1_score(y_test, y_pred, average="weighted", zero_division=0)
        print("as")
        print("Accuracy                                   : %.3f" % accuracy)
        print("Precision                                   : %.3f" % precision)
        print("Recall                                      : %.3f" % recall)
        print("F1-Score                                    : %.3f" % f1)
        print(
            "\nPrecision Recall F1-Score Support Per Class : \n",
            precision_recall_fscore_support(
                y_test, y_pred, average="weighted", zero_division=0
            ),
        )
        print("\nClassification Report                       : ")
        print(classification_report(y_test, y_pred, zero_division=0))
        return accuracy, precision, recall, f1

    def dump_model(self):
        """Dump model to file"""
        if self.knn_path is not None:
            with open(self.knn_path, "wb") as f:
                pickle.dump(self.knn, f)

    def check_face_identity(
        self,
        encodings: np.ndarray,
        *,
        threshold: Optional[int] = 15,
        n_neighbors: Optional[int] = 9
    ) -> Dict[str, int]:
        """Check face identity

        Args:
            encodings (numpy.darray): face encodings
            threshold (int, optional): threshold for face identification Defaults to 0.5.

        Returns:
            identity (Dict[str, int]): return ids with number of images.
        """
        closest_distances = self.knn.kneighbors(
            encodings.reshape(1, -1), n_neighbors=n_neighbors
        )
        ids = {}
        distances = closest_distances[0][0]
        indices = closest_distances[1][0]
        for idx, distance in zip(indices, distances):
            print(idx, self.labels[idx], distance)
            if distance <= threshold:
                if not ids.__contains__(str(self.labels[idx])):
                    ids[str(self.labels[idx])] = 1
                else:
                    ids[str(self.labels[idx])] += 1

        if len(ids) == 0:
            return {"-1": 0}
        else:
            return ids

    def retrain_model(self, new_encodings: np.ndarray, identity: int):
        """Retrain model on new images

        Args:
            new_encodings (numpy.darray): new face encodings
            identity (int): identity of the face
        """
        for new_encoding in new_encodings:
            self.data = np.vstack([self.data, new_encoding])
            self.labels = np.append(self.labels, identity)

        self.knn = self.KNN_Classifier()
        self.dump_model()
