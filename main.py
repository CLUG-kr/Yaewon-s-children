import cv2
import pygame
import time
import random
from deep import build_net
from cam import Camera
from time import sleep

if __name__ == '__main__':
    model_emo = build_net()
    video_camera = Camera(model_emo)

    while True:
        emotion_number = 0
        exit_num = 0
        prev_emo = ""
        while True:
            frame = video_camera.get_face()
            cv2.imshow("image", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                exit_num = 1
                break;
            curr_emo = video_camera.get_emotion()

            if (prev_emo == ""):
                prev_emo = curr_emo
                curr_emo = ""
            else:
                if (prev_emo == curr_emo):
                    emotion_number = emotion_number + 1
                    curr_emo = ""
                else:
                    emotion_number = 0
                    prev_emo = curr_emo
                    curr_emo = ""
            if (emotion_number == 5):
                break;
            sleep(0.1)
        if exit_num == 1:
            break;

        rand = random.randint(1, 3)

        if rand == 1:
            file = "a.mp3"
        elif rand == 2:
            file = "b.mp3"
        elif rand == 3:
            file = "c.mp3"
        music_path = "music/" + prev_emo + "/" + file
        pygame.init()

        pygame.display.set_mode((200, 100))

        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play()

        time.sleep(10)

    cv2.destoryAllWindows()

    """
        while True:
            frame = video_camera.get_face()

            cv2.imshow("image", frame)



            print("11111111"+video_camera.get_emotion())
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            sleep(0.01)

        cv2.destoryAllWindows()
    """