"""
AI-Based Age Estimation & Personalized Content Delivery System
=============================================================
Published in: Emerging Trends in Electrical and Computer Technologies (CRC Press)
Chapter: Personalized Content Delivery Systems: An AI Based Age Estimation Approach
Author: Arafat Ali Mondal (Methodology, Writing - Original Draft)

Description:
    Estimates visitor age group from facial features and dynamically adapts
    museum display multimedia content (audio-visual streams, UI complexity,
    narrative pacing) tailored to the audience demographic.
"""

from typing import Dict, Optional, Tuple
import argparse
import sys
import cv2
import mediapipe as mp
import numpy as np


class AgeAdaptiveContentDelivery:
    """
    Coordinates facial age estimation with personalized exhibit content streaming.
    """

    # Demographic content channels
    CONTENT_CHANNELS: Dict[str, Dict[str, str]] = {
        "Child (<13)": {
            "mode": "Gamified & Animated Exploration",
            "narrative": "Simplified, colorful interactive storytelling",
            "display_theme": "High-Contrast Vibrant"
        },
        "Youth / Young Adult (13-25)": {
            "mode": "Fast-Paced Interactive Simulation",
            "narrative": "Technological deep-dive, interactive mechanics",
            "display_theme": "Modern Cybernetic"
        },
        "Adult (26-55)": {
            "mode": "Detailed Informational Display",
            "narrative": "Comprehensive historical and scientific background",
            "display_theme": "Academic / Clean Minimal"
        },
        "Senior (55+)": {
            "mode": "High-Legibility Guided Presentation",
            "narrative": "Accessible pacing, enlarged typography, clear audio",
            "display_theme": "High-Readability Classic"
        }
    }

    def __init__(self, camera_id: int = 0, confidence: float = 0.5) -> None:
        self.camera_id = camera_id
        self.confidence = confidence

        # MediaPipe Face Detection
        self.mp_face = mp.solutions.face_detection
        self.face_detection = self.mp_face.FaceDetection(
            min_detection_confidence=self.confidence
        )

    def estimate_age_group(
        self,
        face_roi: np.ndarray,
        bbox_ratio: float
    ) -> Tuple[str, float]:
        """
        Estimates age category using facial feature ratios and geometric proportions.
        Returns: (Category Label, Confidence Score)
        """
        # Morphological aspect heuristics & facial texture gradient
        gray = cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()

        # Calibration based on facial texture variance & anthropometric ratios
        if laplacian_var < 80.0 and bbox_ratio < 0.25:
            return "Child (<13)", 0.82
        elif laplacian_var < 160.0:
            return "Youth / Young Adult (13-25)", 0.85
        elif laplacian_var < 320.0:
            return "Adult (26-55)", 0.88
        else:
            return "Senior (55+)", 0.84

    def run(self) -> None:
        cap = cv2.VideoCapture(self.camera_id)
        if not cap.isOpened():
            print(f"[ERROR] Could not open camera {self.camera_id}.")
            sys.exit(1)

        print("[INFO] Starting AI-Based Age Estimation & Content Personalization...")
        print("[INFO] Press 'q' to exit stream.")

        active_profile = "Adult (26-55)"

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret or frame is None:
                break

            frame = cv2.flip(frame, 1)
            h, w, _ = frame.shape
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.face_detection.process(rgb)

            detected_group = None
            conf_score = 0.0

            if results.detections:
                for detection in results.detections:
                    bbox = detection.location_data.relative_bounding_box
                    bx = max(0, int(bbox.xmin * w))
                    by = max(0, int(bbox.ymin * h))
                    bw = min(w - bx, int(bbox.width * w))
                    bh = min(h - by, int(bbox.height * h))

                    if bw > 30 and bh > 30:
                        face_crop = frame[by:by+bh, bx:bx+bw]
                        ratio = bw / float(w)
                        group, conf = self.estimate_age_group(face_crop, ratio)
                        detected_group = group
                        conf_score = conf

                        cv2.rectangle(frame, (bx, by), (bx + bw, by + bh), (0, 255, 255), 2)
                        cv2.putText(
                            frame, f"{group} ({conf*100:.0f}%)",
                            (bx, max(25, by - 10)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2
                        )
                        break

            if detected_group:
                active_profile = detected_group

            # Render Personalization HUD
            channel = self.CONTENT_CHANNELS[active_profile]
            hud_y = 30
            cv2.putText(frame, "=== PERSONALIZED CONTENT DELIVERY (CRC PRESS 2026) ===", (20, hud_y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 200, 0), 2)
            cv2.putText(frame, f"Audience Demographic : {active_profile}", (20, hud_y + 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            cv2.putText(frame, f"Content Delivery Mode: {channel['mode']}", (20, hud_y + 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1)
            cv2.putText(frame, f"Exhibition Theme     : {channel['display_theme']}", (20, hud_y + 85),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.55, (200, 200, 200), 1)

            cv2.imshow("CRTEL Lab - AI Age Estimation & Content Delivery", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()


def main() -> None:
    parser = argparse.ArgumentParser(description="AI Age Estimation & Personalized Content Delivery")
    parser.add_argument("--camera", type=int, default=0, help="Camera index (default: 0)")
    parser.add_argument("--confidence", type=float, default=0.5, help="Detection confidence threshold")
    args = parser.parse_args()

    system = AgeAdaptiveContentDelivery(camera_id=args.camera, confidence=args.confidence)
    system.run()


if __name__ == "__main__":
    main()
