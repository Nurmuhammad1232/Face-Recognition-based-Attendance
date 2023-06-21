from postgres.postgres import *
import logging
import face_recognition
from utils.constants import FR_MODEL
from utils.models import Workers

# FR_variables = {
#     'known_face_encodings' : [],
#     'known_face_ids':[],
#     'known_face_pathes':[],
#     'workers':[]
# }

workers = Workers()


def set_camera_url_file(url):
    with open("last_camera_url.txt", 'w') as file:
        file.write(url)


def get_last_camera_url():
    with open("last_camera_url.txt", 'r') as file:
        url = file.readline()
    try:
        url_int = int(url)
        if str(url_int) == url:
            url = url_int
    except:
        pass
    return url


# Image_path_index = 0
Camera_variables = {
    'frame': [],
    'options': [],
    'running': False,
    'CAMERA_URL': get_last_camera_url()
}


# def collect_known_faces():
#     global FR_variables
#     FR_variables['known_face_pathes'] = get_worker_faces()
#     known_face_encodings = []
#     known_face_ids = []
#     for _,row in FR_variables['known_face_pathes'].iterrows():
#         for columns_name in ['face_path_1','face_path_2','face_path_3']:
#             human_image = face_recognition.load_image_file(row[columns_name])
#             human_face_encoding = face_recognition.face_encodings(human_image, model = FR_MODEL)
#             if len(human_face_encoding)==0:
#                 logging.warning(row[columns_name]," Face not found!!!")
#                 continue
#             known_face_encodings.append(human_face_encoding[0])
#             known_face_ids.append(row['worker_id'])

#     FR_variables['known_face_encodings'] = known_face_encodings
#     FR_variables['known_face_ids'] = known_face_ids

# def UPDATE_FR_variables():
#     global FR_variables
#     FR_variables['workers'] = get_workers()

# def UPDATE_Global_variables():
#     UPDATE_FR_variables()
#     collect_known_faces()
