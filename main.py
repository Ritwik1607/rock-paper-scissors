import random
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import time
import os

# Initialize the webcam
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# Initialize hand detector and other variables
detector = HandDetector(maxHands=1)
timer = 0
stateResult = False
startGame = False
scores = [0, 0]

# Main loop
while True:
    # Check if resources folder exists
    if not os.path.exists("Resources/bg4.png"):
        print("Resource file 'BG.png' not found. Check the path.")
        break

    # Load background image and capture frame
    imgBG = cv2.imread("Resources/bg4.png")
    success, img = cap.read()
    if not success:
        print("Error accessing the camera.")
        break
    
    imgScaled = cv2.resize(img, (0, 0), None, 0.875, 0.875)
    imgScaled = imgScaled[:, 80:480]

    # Detect hand and fingers
    hands, img = detector.findHands(imgScaled)
    if startGame:
        if not stateResult:
            timer = time.time() - initialTime
            cv2.putText(imgBG, str(int(timer)), (605, 435), cv2.FONT_HERSHEY_PLAIN, 6, (255, 0, 255), 4)
            if timer > 3:
                stateResult = True
                timer = 0
                if hands:
                    playerMove = None
                    hand = hands[0]
                    fingers = detector.fingersUp(hand)
                    if fingers == [0, 0, 0, 0, 0]:  # Rock
                        playerMove = 1
                    elif fingers == [1, 1, 1, 1, 1]:  # Paper
                        playerMove = 2
                    elif fingers == [0, 1, 1, 0, 0]:  # Scissors
                        playerMove = 3

                    # AI Move and score calculation
                    randomNumber = random.randint(1, 3)
                    imgAI = cv2.imread(f'Resources/{randomNumber}.png', cv2.IMREAD_UNCHANGED)
                    imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))

                    # Update scores based on moves
                    if (playerMove == 1 and randomNumber == 3) or \
                       (playerMove == 2 and randomNumber == 1) or \
                       (playerMove == 3 and randomNumber == 2):
                        scores[1] += 1
                    elif (playerMove == 3 and randomNumber == 1) or \
                         (playerMove == 1 and randomNumber == 2) or \
                         (playerMove == 2 and randomNumber == 3):
                        scores[0] += 1

    imgBG[234:654, 795:1195] = imgScaled
    if stateResult:
        imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))

    # Display scores
    cv2.putText(imgBG, str(scores[0]), (410, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
    cv2.putText(imgBG, str(scores[1]), (1112, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
    
    # Show background
    cv2.imshow("BG", imgBG)

    # Check for 's' key to start
    key = cv2.waitKey(1)
    if key == ord('s'):
        startGame = True
        initialTime = time.time()
        stateResult = False
    elif key == ord('q'):  # Press 'q' to exit
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
