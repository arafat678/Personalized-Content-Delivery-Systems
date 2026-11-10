# import cv2
# import mediapipe as mp

# def detect_faces(frame):
#     # Initialize MediaPipe face detection
#     mp_face_detection = mp.solutions.face_detection
#     face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.5)

#     # Convert the BGR frame to RGB
#     rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
#     # Make face detections
#     results = face_detection.process(rgb_frame)
    
#     # Check if any faces are detected
#     if results.detections:
#         for detection in results.detections:
#             bboxC = detection.location_data.relative_bounding_box
#             ih, iw, _ = frame.shape
#             bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih), \
#                    int(bboxC.width * iw), int(bboxC.height * ih)
#             # Draw a triangle box around the detected face
#             cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[0]+bbox[2], bbox[1]+bbox[3]), (0, 255, 0), 2)
#         return True
#     else:
#         return False

# def main():
#     # Open webcam
#     cap = cv2.VideoCapture(0)

#     # Flag to indicate if a face is detected
#     face_detected = False

#     # Path to the video file
#     video_path = "C:\\Users\\Administrator\\Downloads\\video2.mp4"
    
#     # Open the video file
#     video_cap = cv2.VideoCapture(video_path)

#     # Main video capture loop
#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             break
        
#         # Flip the frame horizontally for a later selfie-view display
#         frame = cv2.flip(frame, 1)
        
#         # Detect faces and draw triangle box
#         if detect_faces(frame):
#             # Display the frame with face detection
#             cv2.imshow('Face Detection', frame)
#             face_detected = True

#         # Check if a face is detected and play video if face detected
#         if face_detected:
#             ret_video, frame_video = video_cap.read()
#             if ret_video:
#                 cv2.imshow('Video Player', frame_video)
#             else:
#                 print("End of video.")
#                 break

#         if cv2.waitKey(10) & 0xFF == ord('q'):
#             break

#     cap.release()
#     video_cap.release()
#     cv2.destroyAllWindows()

# if __name__ == "__main__":
#     main()



import cv2
import mediapipe as mp

def detect_faces(frame):
    # Initialize MediaPipe face detection
    mp_face_detection = mp.solutions.face_detection
    face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.5)

    # Convert the BGR frame to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Make face detections
    results = face_detection.process(rgb_frame)
    
    # Check if any faces are detected
    if results.detections:
        for detection in results.detections:
            bboxC = detection.location_data.relative_bounding_box
            ih, iw, _ = frame.shape
            bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih), \
                   int(bboxC.width * iw), int(bboxC.height * ih)
            # Draw a triangle box around the detected face
            cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[0]+bbox[2], bbox[1]+bbox[3]), (0, 255, 0), 2)
        return True
    else:
        return False

def main():
    # Open webcam
    cap = cv2.VideoCapture(0)

    # Flag to indicate if a face is detected
    face_detected = False

    # Path to the video file
    video_path = "C:\\Users\\Administrator\\Downloads\\video2.mp4"
    
    # Open the video file
    video_cap = cv2.VideoCapture(video_path)

    # Main video capture loop
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Flip the frame horizontally for a later selfie-view display
        frame = cv2.flip(frame, 1)
        
        # Detect faces and draw triangle box
        if detect_faces(frame):
            # Display the frame with face detection
            cv2.imshow('Face Detection', frame)
            face_detected = True

        # Check if a face is detected and play video if face detected
        if face_detected:
            ret_video, frame_video = video_cap.read()
            if ret_video:
                cv2.imshow('Video Player', frame_video)
            else:
                print("End of video.")
                break
        else:
            print("No face detected. Waiting for face detection to start video playback...")

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    video_cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
