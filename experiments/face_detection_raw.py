import cv2
import mediapipe as mp

# Initialize MediaPipe face detection
mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.5)

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

# Mouse event handler function
def mouse_callback(event, x, y, flags, param):
    global roi_frame
    if event == cv2.EVENT_RBUTTONDOWN:  # Right mouse button clicked
        cv2.destroyWindow("ROI with Face Detection")
        roi_frame = None

# Create "ROI with Face Detection" window
cv2.namedWindow("ROI with Face Detection")

# Set mouse callback function
cv2.setMouseCallback("ROI with Face Detection", mouse_callback)

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
        
        # Make face detections
        results = face_detection.process(rgb_frame)
        
        # Render face detections
        if results.detections:
            for detection in results.detections:
                bboxC = detection.location_data.relative_bounding_box
                ih, iw, _ = roi_frame.shape
                bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih), \
                       int(bboxC.width * iw), int(bboxC.height * ih)
                cv2.rectangle(roi_frame, bbox, (0, 255, 0), 2)
        
        # Display the ROI with face detection
        cv2.imshow('ROI with Face Detection', roi_frame)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

