# import cv2

# cap = cv2.VideoCapture(0)

# while True:
#     ret, frame = cap.read()
#     cv2.imshow('frame', frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# roi = cv2.selectROI(frame)
# print(roi)
# im_cropped = frame[int(roi[1]):int(roi[1] + roi[3]), int(roi[0]):int(roi[0] + roi[2])]
# cv2.imshow("cropped", im_cropped)
# cv2.waitKey(0)

# cap.release()
# cv2.destroyAllWindows()

import cv2

# Function to handle mouse events
def select_roi(event, x, y, flags, param):
    global roi_pts, selecting_roi
    
    if event == cv2.EVENT_LBUTTONDOWN:
        roi_pts = [(x, y)]
        selecting_roi = True
    elif event == cv2.EVENT_LBUTTONUP:
        roi_pts.append((x, y))
        selecting_roi = False
        cv2.rectangle(frame, roi_pts[0], roi_pts[1], (0, 255, 0), 2)
        cv2.imshow("frame", frame)

# Initialize variables
roi_pts = []
selecting_roi = False

cap = cv2.VideoCapture(0)

# Create a window and set mouse callback function
cv2.namedWindow("frame")
cv2.setMouseCallback("frame", select_roi)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    if len(roi_pts) == 2:
        # Extract ROI
        x1, y1 = roi_pts[0]
        x2, y2 = roi_pts[1]
        im_cropped = frame[min(y1, y2):max(y1, y2), min(x1, x2):max(x1, x2)]
        cv2.imshow("cropped", im_cropped)
    
    cv2.imshow("frame", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
