"""
Presence-Activated Interactive Media Trigger
============================================
Developed at Central Research & Training Laboratory (CRTEL), NCSM
Author: Arafat Ali Mondal

Description:
    Triggers dynamic video playback and spatial content switching based on
    human presence in predefined interactive exhibition zones.
"""

import argparse
import os
import sys
import time
import cv2
import mediapipe as mp


class InteractiveMediaTrigger:
    """
    Coordinates human detection events with automated media playback.
    """

    def __init__(self, video_path: str, camera_id: int = 0) -> None:
        self.video_path = video_path
        self.camera_id = camera_id
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(min_detection_confidence=0.5)

    def play_clip(self) -> None:
        """
        Play the media clip when human presence is confirmed.
        """
        if not os.path.exists(self.video_path):
            print(f"[WARN] Video file not found: {self.video_path}. Simulating playback.")
            time.sleep(2)
            return

        print(f"[INFO] Playing interactive media: {self.video_path}")
        cap_vid = cv2.VideoCapture(self.video_path)
        while cap_vid.isOpened():
            ret, vframe = cap_vid.read()
            if not ret:
                break
            cv2.imshow("Interactive Exhibit Display", vframe)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        cap_vid.release()
        cv2.destroyWindow("Interactive Exhibit Display")

    def run(self) -> None:
        cap = cv2.VideoCapture(self.camera_id)
        if not cap.isOpened():
            print(f"[ERROR] Could not open camera {self.camera_id}.")
            sys.exit(1)

        print("[INFO] Presence trigger active. Waiting for visitor... (Press 'q' to quit)")
        cooldown = 0.0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret or frame is None:
                break

            frame = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.pose.process(rgb)

            present = bool(results.pose_landmarks)
            status_color = (0, 255, 0) if present else (0, 0, 255)
            status_text = "VISITOR DETECTED - TRIGGER READY" if present else "AWAITING VISITOR"

            cv2.putText(frame, status_text, (20, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.7, status_color, 2)

            if present and (time.time() - cooldown > 5.0):
                print("[TRIGGER] Visitor detected! Starting interactive experience...")
                cooldown = time.time()
                self.play_clip()

            cv2.imshow("Visitor Detection Monitor", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()


def main() -> None:
    parser = argparse.ArgumentParser(description="Interactive Media Trigger")
    parser.add_argument("--video", type=str, default="sample.mp4", help="Video clip to play")
    parser.add_argument("--camera", type=int, default=0, help="Camera index")
    args = parser.parse_args()

    trigger = InteractiveMediaTrigger(video_path=args.video, camera_id=args.camera)
    trigger.run()


if __name__ == "__main__":
    main()
