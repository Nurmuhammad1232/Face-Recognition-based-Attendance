import logging
import cv2
import threading
import time
from utils.GlobalVariables import Camera_variables
from utils.constants import CAP_PROP_FRAME_WIDTH,CAP_PROP_FRAME_HEIGHT,FREEZE_TIME_OF_CAUGHT_KNOWN_FACE
from Camera.utils import Add_extra_things_to_frame
from postgres.postgres import save_worker_come_time
# import multiprocessing as mp

# def get_capture():
#     cap = cv2.VideoCapture(Camera_variables['CAMERA_URL'])
#     cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAP_PROP_FRAME_WIDTH)
#     cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAP_PROP_FRAME_HEIGHT)
#     cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
#     return cap

# class Camera_MP():
    
#     def __init__(self):        
#         #load pipe for data transmittion to the process
#         self.parent_conn, child_conn = mp.Pipe()
#         #load process
#         self.p = mp.Process(target=self.update, args=(child_conn,Camera_variables['CAMERA_URL']))        
#         #start process
#         # self.p.daemon = True
#         self.p.start()
        
#     def end(self):
#         #send closure request to process
        
#         self.parent_conn.send(2)
        
#     def update(self,conn,camera_url):
#         #load cam into seperate process
        
#         print("Cam Loading...")
#         # cap = cv2.VideoCapture(camera_url,cv2.CAP_FFMPEG)  
#         if isinstance(camera_url,int):
#             cap = cv2.VideoCapture(camera_url)   
#         else:
#             cap = cv2.VideoCapture(camera_url,cv2.CAP_FFMPEG)
#         cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAP_PROP_FRAME_WIDTH)
#         cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAP_PROP_FRAME_HEIGHT)
#         cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
#         print("Cam Loaded...")
#         run = True
#         start_time =time.time()
#         while run:
            
#             #grab frames from the buffer
#             cap.grab()
#             if time.time()-start_time>=3:
#                 break
#             #recieve input data
#             rec_dat = conn.recv()
            
#             if rec_dat == 1:
#                 #if frame requested
#                 ret,frame = cap.read()
#                 conn.send(frame)
#                 start_time =time.time()

                
#             elif rec_dat ==2:
#                 print("CAP RELEASE!!!")
#                 #if close requested
#                 cap.release()
#                 run = False
                
#         print("Camera Connection Closed")        
#         conn.close()
    
    # def get_frame(self):
    #     self.parent_conn.send(1)
    #     frame = self.parent_conn.recv()
    #     self.parent_conn.send(0)
    #     if frame is not None and len(frame)!=0:
    #         return cv2.resize(frame, (CAP_PROP_FRAME_WIDTH,CAP_PROP_FRAME_HEIGHT))
    #     return []

def get_capture():
    if isinstance(Camera_variables['CAMERA_URL'],int):
        cap = cv2.VideoCapture(Camera_variables['CAMERA_URL'])   
    else:
        cap = cv2.VideoCapture(Camera_variables['CAMERA_URL'],cv2.CAP_FFMPEG)
        print(Camera_variables['CAMERA_URL'])
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAP_PROP_FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAP_PROP_FRAME_HEIGHT)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    return cap

class Camera(threading.Thread):
    def __init__(self,name):
        threading.Thread.__init__(self)
        self.name = name
        
    def run(self):
        global Camera_variables
        try:
            cap = get_capture()
            last_succes_time = time.time()
            while Camera_variables['running']:
                if time.time()-last_succes_time>=5:
                    break
                if cap.isOpened():
                    # cap.grab()
                    try:
                        ret, image = cap.read()
                        # fps = cap.get(cv2.CAP_PROP_FPS)
                        # print("{0} fps".format(fps))
                    except Exception as e:
                        break
                    if not ret:
                        cap = get_capture()
                        continue
                    last_succes_time=time.time()
                    Camera_variables['frame'] = cv2.resize(image, (CAP_PROP_FRAME_WIDTH,CAP_PROP_FRAME_HEIGHT))
                    # Camera_variables['frame']  = add_time_to_frame(Camera_variables['frame'])
                    if len(Camera_variables['options'])!=0:
                        try:
                            face_id = Camera_variables['options'][0][-1]
                            # save_image_cashe()
                            big_message = None
                            if face_id is not None:
                                big_message = save_worker_come_time(face_id)
                            Add_extra_things_to_frame(big_message)
                            Camera_variables['options']=[]
                        except Exception as e:
                            print(e)
                        time.sleep(FREEZE_TIME_OF_CAUGHT_KNOWN_FACE)
            cap.release()
            Camera_variables['running'] = False
        except Exception as e:
            cap.release()
            logging.error("Start Camera error :"+str(e))
            Camera_variables['running'] = False
