import cv2
import numpy as np
import os
import time
import handTrackingModule as htm

# Setting up the parameters
previous_time = 0
capture = cv2.VideoCapture(0)  # Turns on the first camera

tools_list = os.listdir('HandControlledPainter/Tools')  # Gets the list of tools from the Tools folder
overlay_list = []

# Looping through the tools list to read and resize each image
for image_path in tools_list:
    image = cv2.imread(f'HandControlledPainter/Tools/{image_path}')
    image = cv2.resize(image, (1366, 120))                          
    overlay_list.append(image)                                      

# Drawing Parameters
toolbar = overlay_list[0]  # Sets the first tool as the default tool
color = (0, 0, 255)
brush_thickness = 20
x_previous, y_previous = 0, 0
frame_canvas = np.zeros((768, 1366, 3), np.uint8)  # Creates a blank canvas for drawing

detector = htm.handDetector(detectionCon=0.85)  # Creates an instance of the hand detector with a detection confidence of 0.75

while True:
    # Importing Frames
    success, frame = capture.read() 
    if not success: break           # Break the loop if the camera fails to read a frame
    frame = cv2.flip(frame, 1)           
    frame = cv2.resize(frame, (1366, 768))
    
    # Finding Hand Landmarks
    frame = detector.findHands(frame)
    landmark_list = detector.findPosition(frame, draw=False)
    
    # Checking Which Fingers Are Up
    ups = ""
    if (len(landmark_list)): 
        tip_index_x, tip_index_y = landmark_list[8][1:]
        tip_middle_x, tip_middle_y = landmark_list[12][1:]
        midpoint = (int((tip_index_x + tip_middle_x)/2), int((tip_index_y + tip_middle_y)/2))
        
        ups = detector.fingerUps()
    
        if ups == "01100":  # Selecting the Tool: Two Fingers Are Up
            x_previous, y_previous = 0, 0
            cv2.circle(frame, midpoint, 50, color, cv2.FILLED)
            
            # Checking for the Click
            if midpoint[1] >= 400:
                if 273 <= midpoint[0] < 546:
                    toolbar = overlay_list[1]
                    color = (0, 0, 255)
                elif 546 <= midpoint[0] < 819:
                    toolbar = overlay_list[2]
                    color = (0, 255, 0)
                elif 819 <= midpoint[0] < 1093:
                    toolbar = overlay_list[3]
                    color = (255, 0, 0)
                elif 1093 <= midpoint[0] <= 1366:
                    toolbar = overlay_list[4]
                    color = (0, 0, 0)
                        
                    
        elif ups == "01000":  # Drawing: One Finger Is Up
            cv2.circle(frame, (tip_index_x, tip_index_y), brush_thickness, color, cv2.FILLED)
            if not x_previous and not y_previous: x_previous, y_previous = tip_index_x, tip_index_y
            
            cv2.line(frame, (x_previous, y_previous), (tip_index_x, tip_index_y), color, brush_thickness)
            cv2.line(frame_canvas, (x_previous, y_previous), (tip_index_x, tip_index_y), color, brush_thickness)
            
            x_previous, y_previous = tip_index_x, tip_index_y
            # print("Drawing Mode")
            
        elif ups == "00001":
            cv2.rectangle(frame, (500, 70), (1150, 20), color, 3)
            brush_thickness = int(np.interp(landmark_list[20][1], (500, 1150), (5, 100)))
            if 1150 >= landmark_list[20][1] >= 500:
                cv2.rectangle(frame, (500, 70), (landmark_list[20][1], 20), color, cv2.FILLED)
                percentage = np.interp(brush_thickness, (5, 100), (0, 100))
                cv2.putText(frame, f'{int(percentage)}%', (landmark_list[20][1] + 10, 50), cv2.FONT_HERSHEY_COMPLEX, 1.5, color, 2)
            cv2.circle(frame, (landmark_list[20][1], landmark_list[20][2]), brush_thickness, color, cv2.FILLED)
        
        else: x_previous, y_previous = 0, 0  # Resetting the previous coordinates when no fingers are up
            
            
    else: x_previous, y_previous = 0, 0  # Resetting the previous coordinates when no hand is detected
        
    frame_gray = cv2.cvtColor(frame_canvas, cv2.COLOR_BGR2GRAY)  # Converting the canvas to grayscale
    _, frame_binary = cv2.threshold(frame_gray, 50, 255, cv2.THRESH_BINARY_INV) # Applying binary thresholding
    frame_binary = cv2.cvtColor(frame_binary, cv2.COLOR_GRAY2BGR)               # Converting the binary image back to BGR format
    frame = cv2.bitwise_and(frame, frame_binary)                                # Applying the binary mask to the frame
    frame = cv2.bitwise_or(frame, frame_canvas)                                 # Combining the frame with the canvas
    
    cv2.putText(frame, "Index for Drawing; index and middle for selection; index, middle and ring for thickness", (10, 530), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 0, 255), 2)
    
    frame[598:718, 0:1366] = toolbar  # Places the toolbar at the top of the frame
    
    # Calculating and Placing FPS
    current_time = time.time()
    fps = 1 / (current_time - previous_time)
    previous_time = current_time              
    cv2.putText(frame, f'FPS: {str(int(fps))}', (10, 70), cv2.FONT_HERSHEY_COMPLEX, 1.5, (0, 255, 255), 2)
    
    
    # Drawing Area
    cv2.rectangle(frame, (5, 548), (1360, 5), (0, 255, 255), 3)
    
    # Displaying the Final Frame
    cv2.imshow("Hand Controlled Painter", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): break # Exit the loop if 'q' is pressed