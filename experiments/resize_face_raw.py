# import cv2
# import mediapipe as mp

# # Initialize MediaPipe face detection
# mp_face_detection = mp.solutions.face_detection
# face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.5)

# # Global variables to store ROI position and flag for mouse dragging
# roi = None
# dragging = False
# offset_x, offset_y = 0, 0

# # Mouse callback function
# def mouse_callback(event, x, y, flags, param):
#     global roi, dragging, offset_x, offset_y

#     # Check for left mouse button press
#     if event == cv2.EVENT_LBUTTONDOWN:
#         # Check if the mouse click is within the ROI window
#         if roi is not None and roi[0] < x < roi[0] + roi[2] and roi[1] < y < roi[1] + roi[3]:
#             dragging = True
#             offset_x = x - roi[0]
#             offset_y = y - roi[1]

#     # Check for left mouse button release
#     elif event == cv2.EVENT_LBUTTONUP:
#         dragging = False

#     # Check for mouse movement while dragging
#     elif event == cv2.EVENT_MOUSEMOVE and dragging:
#         roi = (x - offset_x, y - offset_y, roi[2], roi[3])

# # Open webcam
# cap = cv2.VideoCapture(0)

# # Select ROI
# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break

#     # Flip the frame horizontally for a later selfie-view display
#     frame = cv2.flip(frame, 1)

#     # Display frame for ROI selection
#     cv2.imshow('Select ROI (Press SPACE to confirm selection)', frame)

#     # Check for user input
#     key = cv2.waitKey(1) & 0xFF
#     if key == ord('q'):
#         break
#     elif key == ord(' '):
#         roi = cv2.selectROI("Selected ROI", frame, fromCenter=False, showCrosshair=True)
#         # Double the size of the ROI
#         if roi is not None:
#             roi_x, roi_y, roi_w, roi_h = roi
#             roi_w *= 2
#             roi_h *= 2
#         break

# cv2.destroyAllWindows()

# # Create resizable window for displaying the resized ROI with face detection
# cv2.namedWindow('Resized ROI with Face Detection')
# cv2.setMouseCallback('Resized ROI with Face Detection', mouse_callback)

# # Main video capture loop
# while cap.isOpened():
#     ret, frame = cap.read()
#     if not ret:
#         break

#     # Flip the frame horizontally for a later selfie-view display
#     frame = cv2.flip(frame, 1)

#     # Convert the BGR image to RGB
#     rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

#     # Make face detections
#     results = face_detection.process(rgb_frame)

#     # Initialize variables to store the largest face bounding box
#     max_face_area = 0
#     largest_face_bbox = None

#     # Find the largest face bounding box
#     if results.detections:
#         for detection in results.detections:
#             bboxC = detection.location_data.relative_bounding_box
#             ih, iw, _ = frame.shape
#             bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih), \
#                    int(bboxC.width * iw), int(bboxC.height * ih)
#             # Calculate face area
#             face_area = bbox[2] * bbox[3]
#             # Update largest face bounding box
#             if face_area > max_face_area:
#                 max_face_area = face_area
#                 largest_face_bbox = bbox

#     # Render face detection bounding box
#     if largest_face_bbox is not None:
#         cv2.rectangle(frame, (largest_face_bbox[0], largest_face_bbox[1]), 
#                       (largest_face_bbox[0] + largest_face_bbox[2], largest_face_bbox[1] + largest_face_bbox[3]), 
#                       (0, 255, 0), 1)

#     # Display the frame with face detection
#     cv2.imshow('Face Detection', frame)

#     # Check if ROI is selected and double its size
#     if roi is not None:
#         roi_frame = frame[roi[1]:roi[1] + roi[3], roi[0]:roi[0] + roi[2]]

#         # Convert the BGR image to RGB
#         rgb_roi_frame = cv2.cvtColor(roi_frame, cv2.COLOR_BGR2RGB)

#         # Make face detections on the resized ROI
#         results = face_detection.process(rgb_roi_frame)

#         # Render face detections
#         if results.detections:
#             for detection in results.detections:
#                 bboxC = detection.location_data.relative_bounding_box
#                 ih, iw, _ = roi_frame.shape
#                 bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih), \
#                        int(bboxC.width * iw), int(bboxC.height * ih)
#                 cv2.rectangle(roi_frame, bbox, (0, 255, 0), 1)

#         # Display the resized ROI with face detection
#         cv2.imshow('Resized ROI with Face Detection', roi_frame)

#         # Check for user input
#         key = cv2.waitKey(10) & 0xFF

#         # 'q' key to quit
#         if key == ord('q'):
#             break

# # Release the webcam and close all windows
# cap.release()
# cv2.destroyAllWindows()



# import cv2
# import mediapipe as mp

# # Initialize MediaPipe face detection
# mp_face_detection = mp.solutions.face_detection
# face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.5)

# # Global variables to store ROI position and flag for mouse dragging
# roi = None
# dragging = False
# offset_x, offset_y = 0, 0

# # Mouse callback function
# def mouse_callback(event, x, y, flags, param):
#     global roi, dragging, offset_x, offset_y

#     # Check for left mouse button press
#     if event == cv2.EVENT_LBUTTONDOWN:
#         # Check if the mouse click is within the ROI window
#         if roi is not None and roi[0] < x < roi[0] + roi[2] and roi[1] < y < roi[1] + roi[3]:
#             dragging = True
#             offset_x = x - roi[0]
#             offset_y = y - roi[1]

#     # Check for left mouse button release
#     elif event == cv2.EVENT_LBUTTONUP:
#         dragging = False

#     # Check for mouse movement while dragging
#     elif event == cv2.EVENT_MOUSEMOVE and dragging:
#         roi = (x - offset_x, y - offset_y, roi[2], roi[3])

# # Function to create resizable window with given size and position
# def create_resizable_window(name, width, height, x_pos, y_pos):
#     cv2.namedWindow(name, cv2.WINDOW_NORMAL)
#     cv2.resizeWindow(name, width, height)
#     cv2.moveWindow(name, x_pos, y_pos)

# # Open webcam
# cap = cv2.VideoCapture(0)

# # Select ROI
# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break

#     # Flip the frame horizontally for a later selfie-view display
#     frame = cv2.flip(frame, 1)

#     # Display frame for ROI selection
#     cv2.imshow('Select ROI (Press SPACE to confirm selection)', frame)

#     # Check for user input
#     key = cv2.waitKey(1) & 0xFF
#     if key == ord('q'):
#         break
#     elif key == ord(' '):
#         roi = cv2.selectROI("Selected ROI", frame, fromCenter=False, showCrosshair=True)
#         # Double the size of the ROI
#         if roi is not None:
#             roi_x, roi_y, roi_w, roi_h = roi
#             roi_w *= 2
#             roi_h *= 2
#         break

# cv2.destroyAllWindows()

# # Create resizable window for displaying the resized ROI with face detection
# create_resizable_window('Resized ROI with Face Detection', 640, 480, 100, 100)
# cv2.setMouseCallback('Resized ROI with Face Detection', mouse_callback)

# # Main video capture loop
# while cap.isOpened():
#     ret, frame = cap.read()
#     if not ret:
#         break

#     # Flip the frame horizontally for a later selfie-view display
#     frame = cv2.flip(frame, 1)

#     # Convert the BGR image to RGB
#     rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

#     # Make face detections
#     results = face_detection.process(rgb_frame)

#     # Initialize variables to store the largest face bounding box
#     max_face_area = 0
#     largest_face_bbox = None

#     # Find the largest face bounding box
#     if results.detections:
#         for detection in results.detections:
#             bboxC = detection.location_data.relative_bounding_box
#             ih, iw, _ = frame.shape
#             bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih), \
#                    int(bboxC.width * iw), int(bboxC.height * ih)
#             # Calculate face area
#             face_area = bbox[2] * bbox[3]
#             # Update largest face bounding box
#             if face_area > max_face_area:
#                 max_face_area = face_area
#                 largest_face_bbox = bbox

#     # Render face detection bounding box
#     if largest_face_bbox is not None:
#         cv2.rectangle(frame, (largest_face_bbox[0], largest_face_bbox[1]), 
#                       (largest_face_bbox[0] + largest_face_bbox[2], largest_face_bbox[1] + largest_face_bbox[3]), 
#                       (0, 255, 0), 1)

#     # Display the frame with face detection
#     cv2.imshow('Face Detection', frame)

#     # Check if ROI is selected and double its size
#     if roi is not None:
#         roi_frame = frame[roi[1]:roi[1] + roi[3], roi[0]:roi[0] + roi[2]]

#         # Convert the BGR image to RGB
#         rgb_roi_frame = cv2.cvtColor(roi_frame, cv2.COLOR_BGR2RGB)
        
        
        

#         # Make face detections on the resized ROI
#         results = face_detection.process(rgb_roi_frame)

#         # Render face detections
#         if results.detections:
#             for detection in results.detections:
#                 bboxC = detection.location_data.relative_bounding_box
#                 ih, iw, _ = roi_frame.shape
#                 bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih), \
#                        int(bboxC.width * iw), int(bboxC.height * ih)
#                 cv2.rectangle(roi_frame, bbox, (0, 255, 0), 1)

#         # Display the resized ROI with face detection
#         cv2.imshow('Resized ROI with Face Detection', roi_frame)

#         # Check for user input
#         key = cv2.waitKey(10) & 0xFF

#         # 'q' key to quit
#         if key == ord('q'):
#             break

# # Release the webcam and close all windows
# cap.release()
# cv2.destroyAllWindows()


import cv2
import mediapipe as mp

# Initialize MediaPipe face detection
mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.5)

# Global variables to store ROI position and flag for mouse dragging
roi = None
dragging = False
offset_x, offset_y = 0, 0

# Mouse callback function
def mouse_callback(event, x, y, flags, param):
    global roi, dragging, offset_x, offset_y

    # Check for left mouse button press
    if event == cv2.EVENT_LBUTTONDOWN:
        # Check if the mouse click is within the ROI window
        if roi is not None and roi[0] < x < roi[0] + roi[2] and roi[1] < y < roi[1] + roi[3]:
            dragging = True
            offset_x = x - roi[0]
            offset_y = y - roi[1]

    # Check for left mouse button release
    elif event == cv2.EVENT_LBUTTONUP:
        dragging = False

    # Check for mouse movement while dragging
    elif event == cv2.EVENT_MOUSEMOVE and dragging:
        roi = (x - offset_x, y - offset_y, roi[2], roi[3])

# Function to create resizable window with given size and position
def create_resizable_window(name, width, height, x_pos, y_pos):
    cv2.namedWindow(name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(name, width, height)
    cv2.moveWindow(name, x_pos, y_pos)

# Open webcam
cap = cv2.VideoCapture(0)

# Select ROI
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
        # Double the size of the ROI
        if roi is not None:
            roi_x, roi_y, roi_w, roi_h = roi
            roi_w *= 2
            roi_h *= 2
        break

cv2.destroyAllWindows()

# Create resizable window for displaying the resized ROI with face detection
create_resizable_window('Resized ROI with Face Detection', 640, 480, 100, 100)
cv2.setMouseCallback('Resized ROI with Face Detection', mouse_callback)

# Main video capture loop
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the frame horizontally for a later selfie-view display
    frame = cv2.flip(frame, 1)

    # Convert the BGR image to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Make face detections
    results = face_detection.process(rgb_frame)

    # Initialize variables to store the largest face bounding box
    max_face_area = 0
    largest_face_bbox = None

    # Find the largest face bounding box
    if results.detections:
        for detection in results.detections:
            bboxC = detection.location_data.relative_bounding_box
            ih, iw, _ = frame.shape
            bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih), \
                   int(bboxC.width * iw), int(bboxC.height * ih)
            # Calculate face area
            face_area = bbox[2] * bbox[3]
            # Update largest face bounding box
            if face_area > max_face_area:
                max_face_area = face_area
                largest_face_bbox = bbox

    # Render face detection bounding box
    if largest_face_bbox is not None:
        cv2.rectangle(frame, (largest_face_bbox[0], largest_face_bbox[1]), 
                      (largest_face_bbox[0] + largest_face_bbox[2], largest_face_bbox[1] + largest_face_bbox[3]), 
                      (0, 255, 0), 1)

    # Display the frame with face detection
    cv2.imshow('Face Detection', frame)

    # Check if ROI is selected and double its size
    if roi is not None:
        roi_frame = frame[roi[1]:roi[1] + roi[3], roi[0]:roi[0] + roi[2]]

        # Convert the BGR image to RGB
        rgb_roi_frame = cv2.cvtColor(roi_frame, cv2.COLOR_BGR2RGB)

        # Resize the ROI frame to half its size
        resized_roi_frame = cv2.resize(roi_frame, (0, 0), fx=2, fy=2)

        # Make face detections on the resized ROI
        results = face_detection.process(cv2.cvtColor(resized_roi_frame, cv2.COLOR_BGR2RGB))

        # Render face detections
        if results.detections:
            for detection in results.detections:
                bboxC = detection.location_data.relative_bounding_box
                ih, iw, _ = resized_roi_frame.shape
                bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih), \
                       int(bboxC.width * iw), int(bboxC.height * ih)
                cv2.rectangle(resized_roi_frame, bbox, (0, 255, 0), 1)

        # Display the resized ROI with face detection
        cv2.imshow('Resized ROI with Face Detection', resized_roi_frame)

        # Check for user input
        key = cv2.waitKey(10) & 0xFF

        # 'q' key to quit
        if key == ord('q'):
            break

# Release the webcam and close all windows
cap.release()
cv2.destroyAllWindows()
