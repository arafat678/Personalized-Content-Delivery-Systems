# import vlc

# def play_video(video_path):
#     # Create VLC instance
#     instance = vlc.Instance('--no-xlib')
#     player = instance.media_player_new()
    
#     # Load video
#     media = instance.media_new(video_path)
#     player.set_media(media)
    
#     # Set the window where to render VLC's video output
#     player.set_hwnd(0)  # Pass 0 to disable video output
    
#     # Start playing video
#     player.play()
    
#     # Wait until the video is finished
#     while player.get_state() != vlc.State.Ended:
#         pass
    
#     # Release resources
#     player.release()
#     instance.release()

# if __name__ == "__main__":
#     # Specify the path to your video file
#     video_path = "C:\\Users\\Administrator\\Downloads\\video2.mp4"

#     # Call the function to play the video
#     play_video(video_path)





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

# def play_video(video_path):
#     # Create VLC instance
#     instance = vlc.Instance('--no-xlib')
#     player = instance.media_player_new()
    
#     # Load video
#     media = instance.media_new(video_path)
#     player.set_media(media)
    
#     # Set the window where to render VLC's video output
#     player.set_hwnd(0)  # Pass 0 to disable video output
    
#     # Start playing video
#     player.play()
    
#     # Wait until the video is finished
#     while player.get_state() != vlc.State.Ended:
#         pass
    
#     # Release resources
#     player.release()
#     instance.release()

# def main():
#     # Open webcam
#     cap = cv2.VideoCapture(0)

#     # Flag to indicate if a face is detected
#     face_detected = False

#     # Flag to indicate if video is paused
#     video_paused = False

#     # Path to the video file
#     video_path = "C:\\Users\\Administrator\\Downloads\\video2.mp4"
    
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
#                 play_video(video_path)
#         else:
#             if not video_paused:
#                 # If face not detected and video not paused, pause video
#                 video_paused = True

#         if cv2.waitKey(10) & 0xFF == ord('q'):
#             break

#     cap.release()
#     cv2.destroyAllWindows()

# if __name__ == "__main__":
#     main()


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
#             # Extract bounding box coordinates
#             bboxC = detection.location_data.relative_bounding_box
#             ih, iw, _ = frame.shape
#             bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih), \
#                    int(bboxC.width * iw), int(bboxC.height * ih)
#             # Draw a bounding box around the detected face
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
#     video_paused = True  # Start with video paused

#     # Path to the video file
#     video_path = "C:\\Users\\Administrator\\Downloads\\video2.mp4"

#     # Create VLC instance
#     instance = vlc.Instance('--no-xlib')
#     player = instance.media_player_new()
#     media = instance.media_new(video_path)
#     player.set_media(media)

#     # Main video capture loop
#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             break

#         # Flip the frame horizontally for a later selfie-view display
#         frame = cv2.flip(frame, 1)

#         # Detect faces
#         if detect_faces(frame):
#             # Display the frame with face detection
#             cv2.imshow('Face Detection', frame)
#             face_detected = True
#             if video_paused:
#                 # If face detected and video was paused, resume video
#                 video_paused = False
#                 player.play()  # Start playing the video
#         else:
#             if face_detected:  # Check if a face was previously detected
#                 # If no face detected and video not paused, pause video
#                 video_paused = True
#                 player.pause()

#         if cv2.waitKey(10) & 0xFF == ord('q'):
#             break

#     cap.release()
#     cv2.destroyAllWindows()

# if __name__ == "__main__":
#     main()




# ------modeify__-------
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
    video_path = "C:\\Users\\Administrator\\Downloads\\vieo.mp4"

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
