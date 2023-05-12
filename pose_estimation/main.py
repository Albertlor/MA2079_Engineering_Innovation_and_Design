# https://www.youtube.com/watch?v=aySurynUNAw&t=1930s&ab_channel=BleedAIAcademy

import argparse
import cv2
import time
import json
import curses
import numpy as np
from utils import magnitude
from body_info.pose import Pose
from sound_track.activated_sound import sound_track

ap = argparse.ArgumentParser()
ap.add_argument("-s", "--squat", type=int, help="squatting when doing weightlifting")
ap.add_argument("-p", "--pushups", type=int, help="doing push-ups")
args = vars(ap.parse_args())

squat = args['squat']
pushups = args['pushups']
first_hip = 0

# Initialize the VideoCapture object to read from the webcam.
video = cv2.VideoCapture(0)
video.set(3,1280)
video.set(4,960)

# Initialize a resizable window.
cv2.namedWindow('Frames', cv2.WINDOW_NORMAL)
count_frame = 0
count = 0
g_dir = 0
replay = 0
last_time = time.time()

# For push-ups
cycle = 0
temp_cycle = 0


"""
INITIALIZE SHOULDER 3D COORDINATES
"""
with open('./database/shoulder.json', 'w') as f1:
    json.dump({
        "SHOULDER_0": [0, 0, 0]
    }, f1, indent=4)

"""
INITIALIZE HIP 3D COORDINATES
"""
with open('./database/hip.json', 'w') as f2:
    json.dump({
        "HIP_0": [0, 0, 0]
    }, f2, indent=4)


"""
INITIALIZE KNEE 3D COORDINATES
"""
with open('./database/knee.json', 'w') as f3:
    json.dump({
        "KNEE_0": [0, 0, 0]
    }, f3, indent=4)


# def movement(stdscr):
#     # Clear the screen and set up the curses environment
#     stdscr.clear()
#     curses.curs_set(0)
#     stdscr.nodelay(True)

#     # Loop until the user presses the Escape key
#     while True:
#         # Wait for user input
#         key = stdscr.getch()
#         #, curses.KEY_RIGHT, curses.KEY_UP, curses.KEY_DOWN
#         # Check if the user pressed an arrow key
#         if key in [curses.KEY_LEFT]:
#             motor.left()
#         elif key in [curses.KEY_RIGHT]:
#             motor.right()
#         elif key in [curses.KEY_UP]:
#             motor.forward()
#         elif key in [curses.KEY_DOWN]:
#             motor.backward()
#         # Check if the user pressed the Escape key
#         elif key == 27:
#             break
#         else: 
#             motor.stop()

#         # Refresh the screen
#         stdscr.refresh()

# # Initialize the motor instance
# ENA = 3
# IN1 = 5
# IN2 = 7
# IN3 = 29
# IN4 = 31
# ENB = 26
# motor = Motor(ENA, IN1, IN2, ENB, IN3, IN4)

while True:
    count_frame += 1
    if video.get(cv2.CAP_PROP_FRAME_COUNT) == count_frame:
        video.set(cv2.CAP_PROP_POS_FRAMES, 0)
        count_frame = 1
        replay = 1

    ret, frame = video.read()
    duration = time.time() - last_time

    last_time = time.time()
    fps = str(round((1/duration), 2))

    if ret:
        #frame = imutils.resize(frame, width=800, inter=cv2.INTER_LINEAR)
        cv2.putText(frame, "fps: " + fps, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 1, cv2.LINE_AA)
        
        # Get the width and height of the frame
        frame_height, frame_width, _ =  frame.shape
        
        # Resize the frame while keeping the aspect ratio.
        frame = cv2.resize(frame, (int(frame_width * (640 / frame_height)), 640))
        
        pose = Pose(count_frame, frame, display=False)
        
        # Perform Pose landmark detection.
        frame, landmarks, real_landmarks, shoulder_confidence_index, hip_confidence_index, knee_confidence_index, wrist_confidence_index, elbow_confidence_index, front = pose.detectPose()

        try:
            if front == None:
                cv2.putText(frame, f"Region of Interest is not detected", (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 1, cv2.LINE_AA)

            else:
                with open('./database/hip.json') as f2:
                    config2 = json.load(f2)

                hip = config2[f'HIP_{count_frame}']

                cv2.circle(frame, (int(hip[0]), int(hip[1])), 10, (255, 0, 255), -1)
                if first_hip == 0:
                    first_hip = hip[0]
                else:
                    if hip[0] > first_hip + 100:
                        first_hip = hip[0]
                        cv2.putText(frame, "Moving Right", (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 255), 1, cv2.LINE_AA)
                    elif hip[0] < first_hip - 100:
                        first_hip = hip[0]
                        cv2.putText(frame, "Moving Left", (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 255), 1, cv2.LINE_AA)

                if front == 1:
                    #if count_frame % 50 == 0:
                        #sound_track(r"C:\Users\Albertlor\Academic\MA2079_Engineering_Innovation_and_Design\pose_estimation\sound_track\turn_90deg.mp3")
                    cv2.putText(frame, "Person is facing towards the robot, do a 90deg turn", (50, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 1, cv2.LINE_AA)

                if front == 0:
                    cv2.putText(frame, "Stay in this manner", (50, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 1, cv2.LINE_AA)
                    if squat:
                        if shoulder_confidence_index == 1 and hip_confidence_index == 1:
                            # # Perform the Pose Classification.
                            # frame, _ = classifyPose(landmarks, frame, display=False)
                            with open('./database/shoulder.json') as f1:
                                config1 = json.load(f1)

                            shoulder = config1[f'SHOULDER_{count_frame}']

                            with open('./database/hip.json') as f2:
                                config2 = json.load(f2)

                            hip = config2[f'HIP_{count_frame}']

                            if count == 0:
                                r = np.array(shoulder) - np.array(hip)
                                g_dir = np.multiply(np.array([r[0], r[1]]), 1/(magnitude(r)))
                                count += 1

                            low_back_angle = round(abs(pose.calculateSpineAngleSquat(g_dir, shoulder, hip)), 3)
                            
                            if low_back_angle > 40:
                                #if count_frame % 50 == 0:
                                    #sound_track(r"C:\Users\Albertlor\Academic\MA2079_Engineering_Innovation_and_Design\pose_estimation\sound_track\straighten_your_back.mp3")
                                cv2.putText(frame, "Please strighten your back!", (50, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 1, cv2.LINE_AA)

                            cv2.putText(frame, f"Spine Angle: {low_back_angle}", (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 1, cv2.LINE_AA)

                        else:
                            #if count_frame % 50 == 0:
                                #sound_track(r"C:\Users\Albertlor\Academic\MA2079_Engineering_Innovation_and_Design\pose_estimation\sound_track\move_backward.mp3")
                            cv2.putText(frame, f"Region of Interest is not detected", (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 1, cv2.LINE_AA)

                    if pushups:
                        if shoulder_confidence_index == 1 and hip_confidence_index == 1 and knee_confidence_index == 1 and wrist_confidence_index == 1 and elbow_confidence_index == 1:
                            with open('./database/shoulder.json') as f1:
                                config1 = json.load(f1)

                            shoulder = config1[f'SHOULDER_{count_frame}']

                            with open('./database/hip.json') as f2:
                                config2 = json.load(f2)

                            hip = config2[f'HIP_{count_frame}']

                            with open('./database/knee.json') as f3:
                                config3 = json.load(f3)

                            knee = config3[f'KNEE_{count_frame}']

                            with open('./database/wrist.json') as f4:
                                config4 = json.load(f4)

                            wrist = config4[f'WRIST_{count_frame}']

                            with open('./database/elbow.json') as f5:
                                config5 = json.load(f5)

                            elbow = config5[f'ELBOW_{count_frame}']

                            if count == 0:
                                r = np.array(shoulder) - np.array(hip)
                                g_dir = np.multiply(r, 1/(magnitude(r)))
                                count += 1

                            low_back_angle = round(abs(pose.calculateSpineAnglePush(shoulder, hip, knee)), 3)
                            elbow_angle = round(abs(pose.calculateElbowAngle(wrist, elbow, shoulder)), 3)
                            shoulder_to_floor_distance = round(abs(pose.calculateDistance(wrist, shoulder)), 3)

                            if low_back_angle > 0 and low_back_angle < 20:
                                if shoulder_to_floor_distance < 100:
                                    temp_cycle = 1
                                if temp_cycle == 1:
                                    if shoulder_to_floor_distance > 180:
                                        cycle += 1
                                        print(cycle)
                                        temp_cycle = 0
                                cv2.putText(frame, f"Number of push-ups: {cycle}", (50, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 1, cv2.LINE_AA)
                            else:
                                #if count_frame % 50 == 0:
                                    #sound_track(r"C:\Users\Albertlor\Academic\MA2079_Engineering_Innovation_and_Design\pose_estimation\sound_track\straighten_your_back.mp3")
                                temp_cycle = 0
                                cv2.putText(frame, f"Number of push-ups: {cycle}", (50, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 1, cv2.LINE_AA)
                                cv2.putText(frame, f"Straighten your back", (50, 170), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 1, cv2.LINE_AA)        

                        else:
                            #if count_frame % 50 == 0:
                                #sound_track(r"C:\Users\Albertlor\Academic\MA2079_Engineering_Innovation_and_Design\pose_estimation\sound_track\move_backward.mp3")
                            cv2.putText(frame, f"Region of Interest is not detected", (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 1, cv2.LINE_AA)

            cv2.imshow("Frames", frame)

        except TypeError as e:
            print(e)
            pass

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break