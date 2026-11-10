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
    
    # Add ROI if selected
    if roi is not None:
        roi_x, roi_y, roi_w, roi_h = roi
        roi_frame = frame[roi_y:roi_y+roi_h, roi_x:roi_x+roi_w]
        
        # Convert the BGR image to RGB
        rgb_frame = cv2.cvtColor(roi_frame, cv2.COLOR_BGR2RGB)
        
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
            h, w, c = roi_frame.shape
            x_min = int(x_min * w)
            x_max = int(x_max * w)
            y_min = int(y_min * h)
            y_max = int(y_max * h)
            
            # Draw bounding box around the detected human
            cv2.rectangle(roi_frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
            
            # Calculate the height of the detected person (distance between feet)
            left_ankle = (int(landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x * w), 
                          int(landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y * h))
            right_ankle = (int(landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x * w), 
                           int(landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y * h))
            height_pixels = abs(left_ankle[1] - right_ankle[1])
            height_meters = height_pixels * 0.0254  # Convert pixels to meters
            
            # Display the height
            cv2.putText(roi_frame, f'Height: {height_meters:.2f} meters', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        
        # Display the ROI with human detection
        cv2.imshow('ROI with Human Detection', roi_frame)

    if cv2.waitKey(10) & 0xFF == ord('1'):
        break

cap.release()
cv2.destroyAllWindows()

