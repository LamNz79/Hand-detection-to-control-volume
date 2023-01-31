from gzip import READ
from pickle import FALSE
import cv2
import time
import mediapipe as mp


class hand_detector(object):
    def __init__(self, mode=False, max_hand=2, model_complexity=1, detection_con=0.5, track_con=0.5):
        self.mode = mode
        self.max_hand = max_hand
        self.model_complexity = model_complexity
        self.detection_con = detection_con
        self.track_con = track_con

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            self.mode, self.max_hand, self.model_complexity, self.detection_con, self.track_con)
        self.mp_draw = mp.solutions.drawing_utils

    def find_hands(self, img, draw=True):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)
        if self.results.multi_hand_landmarks:
            for hand_landmark in self.results.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(
                        img, hand_landmark, self.mp_hands.HAND_CONNECTIONS)
        return img

    def find_position(self, img, hand_no=0, draw=False):
        lm_list = []
        if self.results.multi_hand_landmarks:
            my_hand = self.results.multi_hand_landmarks[hand_no]
            for id, lm in enumerate(my_hand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                lm_list.append([id, cx, cy])
                # if id == 0:
                if draw:
                    cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)
            return lm_list


def main():
    cap = cv2.VideoCapture(0)
    c_time = 0
    p_time = 0
    detector = hand_detector()
    lm_list = []
    while True:
        success, img = cap.read()
        img = detector.find_hands(img)
        lm_list = detector.find_position(img)

        if lm_list is not None:
            if len(lm_list) != 0:
                # print(lm_list[5])
                pass

        c_time = time.time()
        fps = 1/(c_time-p_time)
        p_time = c_time
        cv2.putText(img, f'{int(fps)}', (40, 70),
                    cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 3)
        if success:
            cv2.imshow('IMG', img)
        cv2.waitKey(1)
