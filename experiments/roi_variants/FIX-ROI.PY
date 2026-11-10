# Select a region of interest (ROI) from the webcam feed.
# Detect humans using MediaPipe Pose Detection.
# Adjust the coordinates of the detected bounding box to be relative to the ROI.
# Draw the bounding box within the ROI with a fixed green color only when a human is detected within that area

import cv2
import mediapipe as mp
import math

# Initialize MediaPipe Human Detection
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Open webcam
cap = cv2.VideoCapture(0)

# Select ROI
roi = None
while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Flip the frame horizontally for a later selfie-view display
    frame = cv2.flip(frame, 1)
    
    # Display frame for ROI selection
    cv2.imshow('Select ROI (Press SPACE to confirm selection)', frame)
    
    # Check for user input
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord(' '):
        roi = cv2.selectROI("Selected ROI", frame, fromCenter=False, showCrosshair=True)
        break

cv2.destroyAllWindows()

if roi is None:
    print("ROI selection canceled.")
else:
    print("Selected ROI coordinates (x, y, w, h):", roi)


# Main video capture loop
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # Flip the frame horizontally for a later selfie-view display
    frame = cv2.flip(frame, 1)
    
    # Convert the BGR image to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Draw green bounding box based on the ROI coordinates
    if roi is not None:
        roi_x, roi_y, roi_w, roi_h = roi
        cv2.rectangle(frame, (roi_x, roi_y), (roi_x + roi_w, roi_y + roi_h), (0, 255, 0), 2)
    
    # Make detections
    results = pose.process(rgb_frame)
    
    # Render detections
    if results.pose_landmarks:
        # Extract coordinates of all pose landmarks
        landmarks = results.pose_landmarks.landmark
        
        # Get the coordinates of the bounding box
        x_min = min(landmark.x for landmark in landmarks)
        x_max = max(landmark.x for landmark in landmarks)
        y_min = min(landmark.y for landmark in landmarks)
        y_max = max(landmark.y for landmark in landmarks)
        
        # Convert coordinates to pixel values
        h, w, c = frame.shape
        x_min = int(x_min * w)
        x_max = int(x_max * w)
        y_min = int(y_min * h)
        y_max = int(y_max * h)
        
        # Calculate height
        shoulder_left = (landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x * w, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y * h)
        shoulder_right = (landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x * w, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y * h)
        foot_left = (landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].x * w, landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].y * h)
        foot_right = (landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value].x * w, landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value].y * h)
        
        shoulder_distance = math.sqrt((shoulder_right[0] - shoulder_left[0])**2 + (shoulder_right[1] - shoulder_left[1])**2)
        foot_distance = math.sqrt((foot_right[0] - foot_left[0])**2 + (foot_right[1] - foot_left[1])**2)
        
        # Height in pixels
        height = foot_distance - shoulder_distance
        
        # Draw bounding box around the detected human
        cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
        
        # Display height
        cv2.putText(frame, f'Height: {height:.2f} pixels', (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    # Display the frame
    cv2.imshow('Human Detection with Fixed ROI', frame)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

