import logging
import threading
import time
from utils.GlobalVariables import Camera_variables
from faceRecogination.utils import get_face_locations_and_encodings,compare_and_get_face_id
from utils.constants import FREEZE_TIME_OF_CAUGHT_KNOWN_FACE


class FaceRecogination(threading.Thread):
    def __init__(self,name):
        threading.Thread.__init__(self)
        self.name = name
    def run(self):
        while Camera_variables['running']:
            if Camera_variables['frame'] is None or len(Camera_variables['frame'])==0:
                time.sleep(1)
                continue
            try:
                face_locations,face_encodings = get_face_locations_and_encodings()
                if len(face_encodings)!=0:
                    face_id = compare_and_get_face_id(face_encodings[0])
                    Camera_variables['options'].append((*face_locations[0],face_id))
                    time.sleep(FREEZE_TIME_OF_CAUGHT_KNOWN_FACE+2)
            except Exception as e:
                logging.error("Error FaceRecogination: "+str(e))
                time.sleep(1)