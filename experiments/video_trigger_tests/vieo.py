# # import cv2

# # def play_video(video_path):
# #     cap = cv2.VideoCapture(video_path)

# #     if not cap.isOpened():
# #         print("Error: Could not open video file")
# #         return

# #     while cap.isOpened():
# #         ret, frame = cap.read()

# #         if not ret:
# #             break

# #         cv2.imshow('Video Player', frame)
        
# #         # Press 'q' to quit
# #         if cv2.waitKey(25) & 0xFF == ord('q'):
# #             break

# #     cap.release()
# #     cv2.destroyAllWindows()

# # if __name__ == "__main__":
# #     # Specify the path to your video file
# #     video_path ="C:\\Users\\Administrator\\Downloads\\video2.mp4"

# #     # Call the function to play the video
#     play_video(video_path)




# import cv2

# def play_video(video_path):
#     cap = cv2.VideoCapture(video_path)

#     if not cap.isOpened():
#         print("Error: Could not open video file")
#         return

#     # Check if video has audio
#     has_audio = cap.get(cv2.CAP_PROP_AUDIO_OUTPUT)

#     while cap.isOpened():
#         ret, frame = cap.read()

#         if not ret:
#             break

#         cv2.imshow('Video Player', frame)
        
#         # Play audio if available
#         if has_audio:
#             audio_frame = cap.get(cv2.CAP_PROP_POS_MSEC)
#             cap.set(cv2.CAP_PROP_POS_MSEC, audio_frame)
        
#         # Press 'q' to quit
#         if cv2.waitKey(25) & 0xFF == ord('q'):
#             break

#     cap.release()
#     cv2.destroyAllWindows()

# if __name__ == "__main__":
#     # Specify the path to your video file
#     video_path = "C:\\Users\\Administrator\\Downloads\\video2.mp4"

#     # Call the function to play the video
#     play_video(video_path)

# import cv2
# import subprocess

# def has_audio(video_path):
#     cmd = ["ffprobe", "-i", video_path, "-show_streams", "-select_streams", "a:0", "-loglevel", "error"]
#     output = subprocess.check_output(cmd).decode("utf-8")
#     return "channels=" in output

# def play_video(video_path):
#     cap = cv2.VideoCapture(video_path)

#     if not cap.isOpened():
#         print("Error: Could not open video file")
#         return

#     # Check if video has audio
#     has_audio_flag = has_audio(video_path)

#     while cap.isOpened():
#         ret, frame = cap.read()

#         if not ret:
#             break

#         cv2.imshow('Video Player', frame)
        
#         # Play audio if available
#         if has_audio_flag:
#             # Do something to play audio
#             pass
        
#         # Press 'q' to quit
#         if cv2.waitKey(25) & 0xFF == ord('q'):
#             break

#     cap.release()
#     cv2.destroyAllWindows()

# if __name__ == "__main__":
#     # Specify the path to your video file
#     video_path = "C:\\Users\\Administrator\\Downloads\\video2.mp4"

#     # Call the function to play the video
#     play_video(video_path)


# import vlc

# def play_video(video_path):
#     # Create VLC instance for video
#     instance = vlc.Instance('--no-xlib')
#     player = instance.media_player_new()
    
#     # Load video
#     media = instance.media_new(video_path)
#     player.set_media(media)
    
#     # Set the window id where to render VLC's video output
#     player.set_hwnd(0)  # Pass 0 to disable video output
    
#     # Start playing video
#     player.play()
    
#     # Wait for the video to finish playing
#     while player.is_playing():
#         pass
    
#     # Release player and instance
#     player.release()
#     instance.release()

# if __name__ == "__main__":
#     # Specify the path to your video file
#     video_path = "C:\\Users\\Administrator\\Downloads\\video2.mp4"

#     # Call the function to play the video
#     play_video(video_path)
