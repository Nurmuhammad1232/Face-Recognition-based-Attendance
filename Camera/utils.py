import cv2
from utils.GlobalVariables import Camera_variables,workers
from utils.constants import SCALE_PERCENT,UNKNOWN_FACE_TEXT
from datetime import datetime
import copy

def Add_extra_things_to_frame(big_message):
    try:
        global Camera_variables,SCALE_PERCENT
        top,right,bottom,left,face_id = Camera_variables['options'][0]
        top*=SCALE_PERCENT
        right*=SCALE_PERCENT
        bottom*=SCALE_PERCENT
        left*=SCALE_PERCENT
        Camera_variables['frame'] = draw_border(img = Camera_variables['frame'].copy(),
                                                opt1 = (left, top),
                                                opt2 = (right, bottom),
                                                color=(255,255,255),
                                                thickness=5,
                                                r=10,
                                                d = 20
                                                )
        Camera_variables['frame'] = increse_contrast(Camera_variables['frame'])
        Camera_variables['frame'] = increase_brightness(Camera_variables['frame'])
        text = UNKNOWN_FACE_TEXT
        if face_id is not None:
            row = workers[workers.index==face_id].iloc[0]
            name = row['name']
            fname = row['f_name']
            text = name+' '+fname

        font = cv2.FONT_HERSHEY_DUPLEX
        textsize = cv2.getTextSize(text, font, 2, 1)[0]
        textX = int((Camera_variables['frame'].shape[1] - textsize[0]) / 2)
        cv2.rectangle(Camera_variables['frame'], (0, 0), (1920, 140), (255, 255, 255), -1)
        cv2.putText(Camera_variables['frame'], text, (textX,120), font, 2, (0,0,139), 1)

        if big_message is not None:
            put_big_text_to_frame(big_message)

    except Exception as e:
        print("Add_extra_things_to_frame",e)

def put_big_text_to_frame(text):
    font = cv2.FONT_HERSHEY_COMPLEX
    textsize = cv2.getTextSize(text, font, 2, 2)[0]
    textX = int((Camera_variables['frame'].shape[1] - textsize[0]) / 2)
    cv2.rectangle(Camera_variables['frame'], (0, 0), (1920, 70), (0,0,139), -1)
    cv2.putText(Camera_variables['frame'], text, (textX,50), font, 2, (255, 255, 255), 2)

def draw_border(img, opt1, opt2, color, thickness, r, d):
    x1,y1, = opt1
    x2,y2 = opt2

    # Top left
    cv2.line(img, (x1 + r, y1), (x1 + r + d, y1), color, thickness)
    cv2.line(img, (x1, y1 + r), (x1, y1 + r + d), color, thickness)
    cv2.ellipse(img, (x1 + r, y1 + r), (r, r), 180, 0, 90, color, thickness)

    # Top right
    cv2.line(img, (x2 - r, y1), (x2 - r - d, y1), color, thickness)
    cv2.line(img, (x2, y1 + r), (x2, y1 + r + d), color, thickness)
    cv2.ellipse(img, (x2 - r, y1 + r), (r, r), 270, 0, 90, color, thickness)

    # Bottom left
    cv2.line(img, (x1 + r, y2), (x1 + r + d, y2), color, thickness)
    cv2.line(img, (x1, y2 - r), (x1, y2 - r - d), color, thickness)
    cv2.ellipse(img, (x1 + r, y2 - r), (r, r), 90, 0, 90, color, thickness)

    # Bottom right
    cv2.line(img, (x2 - r, y2), (x2 - r - d, y2), color, thickness)
    cv2.line(img, (x2, y2 - r), (x2, y2 - r - d), color, thickness)
    cv2.ellipse(img, (x2 - r, y2 - r), (r, r), 0, 0, 90, color, thickness)
    return img


def increse_contrast(img):
    lab= cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l_channel, a, b = cv2.split(lab)

    # Applying CLAHE to L-channel
    # feel free to try different values for the limit and grid size:
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    cl = clahe.apply(l_channel)

    # merge the CLAHE enhanced L-channel with the a and b channel
    limg = cv2.merge((cl,a,b))

    # Converting image from LAB Color model to BGR color spcae
    enhanced_img = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

    # Stacking the original image with the enhanced image
    # result = np.hstack((img, enhanced_img))
    return enhanced_img

def increase_brightness(img, value=30):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    lim = 255 - value
    v[v > lim] = 255
    v[v <= lim] += value

    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return img


# def add_time_to_frame(frame):
#     font = cv2.FONT_HERSHEY_DUPLEX
#     local = datetime.now()
#     dt = local.strftime("%m-%d-%Y, %H:%M:%S")
#     frame = cv2.putText(frame, dt,
#                             (10,40),
#                             font, 1,
#                             (0,0,139),
#                             2)

#     return frame

# def save_image_cashe():
#     try:
#         global Camera_variables,FR_variables,SCALE_PERCENT,Image_path_index
#         img = copy.deepcopy(Camera_variables['frame'])
#         top,right,bottom,left,_ =  copy.deepcopy(Camera_variables['options'][0])
#         top*=SCALE_PERCENT
#         right*=SCALE_PERCENT
#         bottom*=SCALE_PERCENT
#         left*=SCALE_PERCENT
#         crop_img = img[top:bottom, left:right]
#         Image_path_index = (Image_path_index+1)%3
#         image_path = Image_Main_Path/(str(Image_path_index)+'.png')
#         cv2.imwrite(str(image_path),crop_img)
#     except Exception as e:
#         print("save_image_cashe",e)