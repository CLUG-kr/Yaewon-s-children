
import cv2
import numpy as np

from collections import deque

import tflearn
from tflearn.data_preprocessing import ImagePreprocessing

emotions = ["Fear", "Happy", "Sad", "Surprise", "Neutral"]

gy_offset = 0
gx_offset = 0


class Camera(object):
    def __init__(self,model:tflearn.DNN):
        print("get model")
        self.model_emo=model
        print("load model")
        self.video = cv2.VideoCapture(0)
        # print(self.video.isOpened())
        self.face_cascade = cv2.CascadeClassifier(
            'haarcascade_frontalface_default.xml')
        self.emotion_queue=deque(maxlen=10)
        self.emotion=""
        self.emotion_prob=0
        self.prediction=0
        self.processedimg=0
        self.emotion_idx=0

    def __del__(self):
        self.video.release()

    def get_emotion(self):
        return self.emotion;

    def get_face(self):
        global gy_offset
        global gx_offset
        success, frame = self.video.read()
        grayed = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(grayed, 1.3, 5)
        for (x, y, w, h) in faces:

            y_offset = y
            x_offset = x+w

            gy_offset = y_offset
            gx_offset = x_offset
            '''
            if grayed.shape[0] < y_offset :
                pass
            '''
            roi_gray = grayed[y:y + h, x:x + w]

            image_scaled = np.array(cv2.resize(roi_gray, (48, 48)), dtype=float)
            image_processed = image_scaled.flatten()
            processedimage = image_processed.reshape([-1, 48, 48, 1])
            # print("predict image")
            prediction = self.model_emo.predict(processedimage)

            # print("gender prediction! : " + str(list(prediction_gender)))
            emotion_probability, emotion_index = max((val, idx) for (idx, val) in enumerate(prediction[0]))
            self.emotion = emotions[emotion_index]
            # self.emotion_queue.appendleft((emotion_probability, emotion))

            print(self.emotion)

        # 영상에 말풍선을 추가.

        if self.emotion != "" :
            img_path = "img/" + self.emotion + ".png"
            overlay_img = cv2.imread(img_path,cv2.IMREAD_UNCHANGED)
            resize_overlay_img = cv2.resize(overlay_img,(200,200))

            y1, y2 = gy_offset, gy_offset + resize_overlay_img.shape[0]
            x1, x2 = gx_offset, gx_offset + resize_overlay_img.shape[1]

            alpha_s = resize_overlay_img[:, :, 3] / 255.0
            alpha_l = 1.0 - alpha_s
            type(frame)
            print("x1,x2:",x1,",",x2,"y1,y2",y1,",",y2)
            try :
                for c in range(0, 3):
                    frame[y1:y2, x1:x2, c] = (alpha_s * resize_overlay_img[:, :, c] +
                                              alpha_l * frame[y1:y2, x1:x2, c])
            except:
                pass
        return frame



