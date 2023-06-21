import cv2
from utils.constants import SCALE_PERCENT
from utils.GlobalVariables import Camera_variables,workers
import face_recognition
from utils.constants import FR_MODEL,FR_TOLERANCE
import numpy as np

def resize_frame(frame):
    fx = fy = SCALE_PERCENT / 100.0
    frame = cv2.resize(frame, (0, 0), fx=fx, fy=fy)
    return frame

def get_face_locations_and_encodings():
    global Camera_variables
    if Camera_variables['frame'] is None or len(Camera_variables['frame'])==0:
        return [],[]
    small_frame = resize_frame(frame = Camera_variables['frame'])
    rgb_small_frame = small_frame[:, :, ::-1]
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(face_image = rgb_small_frame, 
                                                        known_face_locations = face_locations, 
                                                        num_jitters=1, 
                                                        model = FR_MODEL)
    return face_locations,face_encodings

def compare_and_get_face_id(face_encoding):
    global workers
    face_id = None
    if not workers['face_encodings'].empty:
        matches = face_recognition.compare_faces(list(workers['face_encodings'].values), face_encoding,tolerance = FR_TOLERANCE)
        face_distances = face_recognition.face_distance(list(workers['face_encodings'].values), face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            face_id = workers.iloc[best_match_index].name
    return face_id
