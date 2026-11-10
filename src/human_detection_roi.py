"""
Interactive Human Detection with Region of Interest (ROI) Tracking
===================================================================
Developed at Central Research & Training Laboratory (CRTEL), NCSM
Author: Arafat Ali Mondal

Description:
    Real-time vision pipeline combining manual Region-of-Interest (ROI)
    selection with MediaPipe Pose estimation to track human presence,
    bounding coordinates, and spatial engagement within defined zones.
"""

from typing import Optional, Tuple
import argparse
import sys
import cv2
import mediapipe as mp
import numpy as np


class HumanDetectorROI:
    """
    Real-time human pose and ROI detector using MediaPipe and OpenCV.
    """

    def __init__(
        self,
        min_detection_confidence: float = 0.5,
        min_tracking_confidence: float = 0.5,
        camera_id: int = 0
    ) -> None:
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence
        self.camera_id = camera_id

        # MediaPipe pose pipeline
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=self.min_detection_confidence,
            min_tracking_confidence=self.min_tracking_confidence
        )

    def select_roi(self, cap: cv2.VideoCapture) -> Optional[Tuple[int, int, int, int]]:
        """
        Interactive ROI selection via OpenCV GUI.
        Press SPACE or ENTER to confirm, or 'c' / ESC to cancel.
        """
        print("[INFO] Initializing webcam for ROI selection...")
        ret, frame = cap.read()
        if not ret or frame is None:
            print("[ERROR] Failed to read from webcam.")
            return None

        frame = cv2.flip(frame, 1)
        window_title = "Select ROI - Drag Box & Press SPACE/ENTER (ESC to skip)"
        roi = cv2.selectROI(window_title, frame, fromCenter=False, showCrosshair=True)
        cv2.destroyWindow(window_title)

        x, y, w, h = roi
        if w > 0 and h > 0:
            print(f"[INFO] Selected ROI: x={x}, y={y}, w={w}, h={h}")
            return roi
        print("[WARN] No valid ROI selected. Running across full frame.")
        return None

    def run(self, interactive_roi: bool = True) -> None:
        """
        Execute the live human detection and ROI tracking loop.
        """
        cap = cv2.VideoCapture(self.camera_id)
        if not cap.isOpened():
            print(f"[ERROR] Could not open camera device {self.camera_id}.")
            sys.exit(1)

        roi = self.select_roi(cap) if interactive_roi else None

        print("[INFO] Starting real-time detection stream. Press 'q' to exit.")

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret or frame is None:
                break

            # Mirror frame horizontally for intuitive interaction
            frame = cv2.flip(frame, 1)
            h, w, _ = frame.shape

            # Target detection region
            if roi is not None:
                rx, ry, rw, rh = roi
                roi_frame = frame[ry:ry+rh, rx:rx+rw]
                # Draw ROI border on display
                cv2.rectangle(frame, (rx, ry), (rx+rw, ry+rh), (255, 128, 0), 2)
                cv2.putText(
                    frame, "ACTIVE ROI ZONE", (rx, max(20, ry - 10)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 128, 0), 2
                )
                process_frame = roi_frame
                offset_x, offset_y = rx, ry
            else:
                process_frame = frame
                offset_x, offset_y = 0, 0

            # Convert to RGB for MediaPipe inference
            rgb_frame = cv2.cvtColor(process_frame, cv2.COLOR_BGR2RGB)
            results = self.pose.process(rgb_frame)

            # Analyze detections
            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark
                ph, pw, _ = process_frame.shape

                # Compute bounding box
                xs = [lm.x for lm in landmarks if lm.visibility > 0.3]
                ys = [lm.y for lm in landmarks if lm.visibility > 0.3]

                if xs and ys:
                    bbox_x1 = int(min(xs) * pw) + offset_x
                    bbox_x2 = int(max(xs) * pw) + offset_x
                    bbox_y1 = int(min(ys) * ph) + offset_y
                    bbox_y2 = int(max(ys) * ph) + offset_y

                    # Render detection bounding box and status
                    cv2.rectangle(frame, (bbox_x1, bbox_y1), (bbox_x2, bbox_y2), (0, 255, 0), 2)
                    cv2.putText(
                        frame, "HUMAN DETECTED", (bbox_x1, max(25, bbox_y1 - 10)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2
                    )

                # Render skeleton overlay
                self.mp_drawing.draw_landmarks(
                    process_frame,
                    results.pose_landmarks,
                    self.mp_pose.POSE_CONNECTIONS,
                    self.mp_drawing.DrawingSpec(color=(0, 255, 255), thickness=2, circle_radius=2),
                    self.mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2)
                )

            # Display real-time output
            cv2.imshow("CRTEL Lab - Human Detection & Spatial Tracking", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
        print("[INFO] Stream terminated cleanly.")


def main() -> None:
    parser = argparse.ArgumentParser(description="CRTEL Lab: Human Detection & ROI Tracking")
    parser.add_argument("--camera", type=int, default=0, help="Camera device index (default: 0)")
    parser.add_argument("--confidence", type=float, default=0.5, help="Detection confidence threshold")
    parser.add_argument("--no-roi", action="store_true", help="Skip interactive ROI selection")
    args = parser.parse_args()

    detector = HumanDetectorROI(
        min_detection_confidence=args.confidence,
        min_tracking_confidence=args.confidence,
        camera_id=args.camera
    )
    detector.run(interactive_roi=not args.no_roi)


if __name__ == "__main__":
    main()

