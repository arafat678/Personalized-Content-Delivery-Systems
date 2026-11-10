import cv2

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Failed to open camera.")
else:
    while True:
        ret, frame = cap.read()
        frame = cv2.resize(frame, (640, 480))
        roi=cv2.selectROI("Select ROI",frame)
        
        
        if not ret:
            print("Error: Failed to capture frame.")
            break
        
        frame = cv2.resize(frame, (640, 480))
        
        cv2.imshow("Video", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Release the camera
    cap.release()
    cv2.destroyAllWindows()

# import cv2

# # Open webcam
# cap = cv2.VideoCapture(0)

# # Check if the camera is opened successfully
# if not cap.isOpened():
#     print("Error: Failed to open camera.")
# else:
#     # Read a frame from the camera
#     ret, frame = cap.read()
    
#     # Check if the frame is captured successfully
#     if not ret:
#         print("Error: Failed to capture frame.")
#     else:
#         # Resize the frame
#         frame = cv2.resize(frame, (640, 480))
        
#         # Select ROI
#         roi = cv2.selectROI("Select ROI", frame)
        
#         # Print the coordinates of the selected ROI
#         print("Selected ROI coordinates (x, y, w, h):", roi)
        
#         # Main video capture loop
#         while True:
#             # Read a frame from the camera
#             ret, frame = cap.read()
            
#             # Check if the frame is captured successfully
#             if not ret:
#                 print("Error: Failed to capture frame.")
#                 break
            
#             # Resize the frame
#             frame = cv2.resize(frame, (640, 480))
#             roi = frame[46:385,108:504]
            
#             # Display the frame
#             cv2.imshow("Video", frame)
#             cv2.imshow("Video roi", roi)
            
#             # Break the loop if 'q' is pressed
#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 break
    
#     # Release the camera
#     cap.release()
#     cv2.destroyAllWindows()
