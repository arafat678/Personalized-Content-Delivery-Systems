# import cv2
# import mediapipe as mp
# import vlc

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
    
#     # Create a VLC media player instance
#     vlc_instance = vlc.Instance('--no-xlib')

#     # Create a VLC media player object
#     player = vlc_instance.media_player_new()

#     # Load the video file
#     media = vlc_instance.media_new(video_path)
#     player.set_media(media)

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
#             # Start video playback
#             player.play()

#             # Wait for video playback to finish
#             while True:
#                 # Check if the video has ended
#                 if player.get_state() == vlc.State.Ended:
#                     print("End of video.")
#                     break

#         if cv2.waitKey(10) & 0xFF == ord('q'):
#             break

#     # Release resources
#     player.release()
#     cap.release()
#     cv2.destroyAllWindows()

# if __name__ == "__main__":
#     main()

# ---------------------------alll ok------
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

#     # Flag to indicate if video is paused
#     video_paused = False

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
#             if video_paused:
#                 # If face detected and video was paused, resume video
#                 video_paused = False
#                 video_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Rewind video
#         else:
#             if not video_paused:
#                 # If face not detected and video not paused, pause video
#                 video_paused = True

#         # Check if a face is detected and play video if face detected
#         if face_detected and not video_paused:
#             ret_video, frame_video = video_cap.read()
#             if ret_video:
#                 cv2.imshow('Video Player', frame_video)
#             else:
#                 print("End of video.")
#                 break
#         elif not face_detected:
#             print("No face detected. Waiting for face detection to start video playback...")

#         if cv2.waitKey(10) & 0xFF == ord('q'):
#             break

#     cap.release()
#     video_cap.release()
#     cv2.destroyAllWindows()

# if __name__ == "__main__":
#     main()
# ---------------add sound-----

import cv2
import mediapipe as mp
import vlc

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
        return True
    else:
        return False

def main():
    # Open webcam
    cap = cv2.VideoCapture(0)

    # Flag to indicate if video is paused
    video_paused = True

    # Path to the video file
    video_path = "C:\\Users\\Administrator\\Downloads\\video2.mp4"

    # Create VLC instance
    instance = vlc.Instance('--no-xlib')
    player = instance.media_player_new()
    media = instance.media_new(video_path)
    player.set_media(media)

    # Main video capture loop
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Flip the frame horizontally for a later selfie-view display
        frame = cv2.flip(frame, 1)

        # Detect faces
        if detect_faces(frame):
            # Display the frame with face detection
            cv2.imshow('Face Detection', frame)
            if video_paused:
                # If face detected and video was paused, resume video
                video_paused = False
                player.play()  # Start playing the video
        else:
            if not video_paused:
                # If no face detected and video not paused, pause video
                video_paused = True
                player.pause()

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()