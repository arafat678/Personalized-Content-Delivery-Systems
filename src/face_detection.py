"""
Real-Time Multi-Person Face Detection & Coordinate Extraction
============================================================
Developed at Central Research & Training Laboratory (CRTEL), NCSM
Author: Arafat Ali Mondal

Description:
    Real-time face detection pipeline using MediaPipe Face Detection for
    visitor presence sensing, proximity gating, and interactive triggering.
"""

import argparse
import sys
import cv2
import mediapipe as mp


class RealTimeFaceDetector:
    """
    MediaPipe-backed face detector optimized for interactive kiosks.
    """

    def __init__(self, min_confidence: float = 0.5, camera_id: int = 0) -> None:
        self.min_confidence = min_confidence
        self.camera_id = camera_id
        self.mp_face = mp.solutions.face_detection
        self.mp_drawing = mp.solutions.drawing_utils
        self.face_detection = self.mp_face.FaceDetection(
            min_detection_confidence=self.min_confidence
        )

    def run(self) -> None:
        cap = cv2.VideoCapture(self.camera_id)
        if not cap.isOpened():
            print(f"[ERROR] Unable to open camera {self.camera_id}.")
            sys.exit(1)

        print("[INFO] Face detection running. Press 'q' to stop.")

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret or frame is None:
                break

            frame = cv2.flip(frame, 1)
            h, w, _ = frame.shape

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.face_detection.process(rgb_frame)

            detected_count = 0
            if results.detections:
                detected_count = len(results.detections)
                for detection in results.detections:
                    bbox = detection.location_data.relative_bounding_box
                    score = detection.score[0]

                    bx = int(bbox.xmin * w)
                    by = int(bbox.ymin * h)
                    bw = int(bbox.width * w)
                    bh = int(bbox.height * h)

                    cv2.rectangle(frame, (bx, by), (bx + bw, by + bh), (0, 255, 0), 2)
                    label = f"Face: {score:.2f}"
                    cv2.putText(
                        frame, label, (bx, max(20, by - 10)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2
                    )

            # Overlay stats
            cv2.putText(
                frame, f"Faces Detected: {detected_count}", (20, 35),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2
            )

            cv2.imshow("CRTEL Lab - Real-Time Face Detection", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()


def main() -> None:
    parser = argparse.ArgumentParser(description="Real-Time Face Detection")
    parser.add_argument("--camera", type=int, default=0, help="Camera index")
    parser.add_argument("--confidence", type=float, default=0.5, help="Confidence threshold")
    args = parser.parse_args()

    detector = RealTimeFaceDetector(min_confidence=args.confidence, camera_id=args.camera)
    detector.run()


if __name__ == "__main__":
    main()
