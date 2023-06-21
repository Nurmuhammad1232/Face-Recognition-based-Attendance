from Camera.camera import Camera
from utils.GlobalVariables import Camera_variables, get_last_camera_url
from faceRecogination.faceRecogination import FaceRecogination

CF_DICT = {
    'CAP': None,
    'FR_obj': None
}


def restart_CF_DICT_VARIABLES():
    Camera_variables['running'] = False
    if CF_DICT['CAP'] is not None:
        CF_DICT['CAP'].join()
    if CF_DICT['FR_obj'] is not None:
        CF_DICT['FR_obj'].join()
    Camera_variables['CAMERA_URL'] = get_last_camera_url()
    create_new_CF_DICT_VARIABLES()
    Camera_variables['running'] = True
    CF_DICT['CAP'].start()
    CF_DICT['FR_obj'].start()


def create_new_CF_DICT_VARIABLES():
    CF_DICT['CAP'] = Camera('camera_thread')
    CF_DICT['CAP'].daemon = True
    CF_DICT['FR_obj'] = FaceRecogination('face_thread')
    CF_DICT['FR_obj'].daemon = True
