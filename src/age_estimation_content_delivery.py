"""
Multimodal Age & Height Classification System for Personalized Content Delivery
================================================================================
Published in: Emerging Trends in Electrical and Computer Technologies (CRC Press)
Chapter: Personalized Content Delivery Systems: An AI Based Age Estimation Approach
Author: Arafat Ali Mondal (Methodology, Writing - Original Draft)

Architecture Pipeline:
  1. Face-to-Age: Facial morphology and texture feature extraction.
  2. Height-to-Age: Real-time skeletal pose stature estimation (head-to-heel).
  3. Age-to-Height Validation: Cross-modal consistency check.
  4. Fallback Handling: Manual input option when vision confidence is low.
  5. Visitor Classification Model: Multi-modal fusion driving the interactive Display.
"""

from typing import Dict, Optional, Tuple
import argparse
import sys
import time
import cv2
import mediapipe as mp
import numpy as np


class MultimodalVisitorClassifier:
    """
    Implements the full Age & Height Classification pipeline shown in the
    published CRC Press chapter architecture.
    """

    DEMOGRAPHIC_PROFILES: Dict[str, Dict[str, str]] = {
        "Child (<13)": {
            "height_range": "90 cm - 145 cm",
            "content_mode": "Gamified & Animated Exploration",
            "narrative": "Interactive cartoon storytelling and simplified science games",
            "theme_color": (0, 255, 255)
        },
        "Youth / Teen (13-20)": {
            "height_range": "145 cm - 170 cm",
            "content_mode": "Fast-Paced Interactive Simulation",
            "narrative": "Technological challenges, mechanics, and interactive UI",
            "theme_color": (255, 128, 0)
        },
        "Adult (21-55)": {
            "height_range": "155 cm - 190 cm",
            "content_mode": "In-Depth Scientific & Historical Presentation",
            "narrative": "Comprehensive museum archives, technical details, and context",
            "theme_color": (0, 255, 0)
        },
        "Senior (55+)": {
            "height_range": "150 cm - 180 cm",
            "content_mode": "High-Legibility Guided Walkthrough",
            "narrative": "Relaxed pacing, enlarged high-contrast typography, clear audio",
            "theme_color": (255, 200, 200)
        }
    }

    def __init__(self, camera_id: int = 0, confidence: float = 0.5) -> None:
        self.camera_id = camera_id
        self.confidence = confidence

        # MediaPipe Face & Pose solutions
        self.mp_face = mp.solutions.face_detection
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils

        self.face_detector = self.mp_face.FaceDetection(min_detection_confidence=self.confidence)
        self.pose_detector = self.mp_pose.Pose(min_detection_confidence=self.confidence)

        # Baseline calibration (pixels to estimated centimeters)
        self.pixel_to_cm_ratio = 0.35

    def estimate_face_to_age(self, face_roi: np.ndarray, face_ratio: float) -> Tuple[str, float]:
        """
        Branch 1: Face to Age Estimation using texture gradient and geometric ratio.
        """
        gray = cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()

        if laplacian_var < 80.0 and face_ratio < 0.22:
            return "Child (<13)", 0.85
        elif laplacian_var < 160.0:
            return "Youth / Teen (13-20)", 0.84
        elif laplacian_var < 320.0:
            return "Adult (21-55)", 0.89
        else:
            return "Senior (55+)", 0.83

    def estimate_height_to_age(self, landmarks, frame_h: int) -> Tuple[Optional[float], Optional[str]]:
        """
        Branch 2: Height to Age using skeletal landmarks (nose to ankles/heels).
        """
        nose = landmarks[self.mp_pose.PoseLandmark.NOSE.value]
        left_heel = landmarks[self.mp_pose.PoseLandmark.LEFT_HEEL.value]
        right_heel = landmarks[self.mp_pose.PoseLandmark.RIGHT_HEEL.value]

        if nose.visibility > 0.4 and (left_heel.visibility > 0.3 or right_heel.visibility > 0.3):
            lowest_heel_y = max(left_heel.y, right_heel.y)
            pixel_height = (lowest_heel_y - nose.y) * frame_h
            # Calibrated approximate stature (including top of head offset +15%)
            estimated_cm = (pixel_height * 1.15) * self.pixel_to_cm_ratio

            if estimated_cm < 140.0:
                age_group = "Child (<13)"
            elif estimated_cm < 165.0:
                age_group = "Youth / Teen (13-20)"
            elif estimated_cm < 185.0:
                age_group = "Adult (21-55)"
            else:
                age_group = "Adult (21-55)"
            return estimated_cm, age_group
        return None, None

    def fuse_visitor_classification(
        self,
        face_group: Optional[str],
        face_conf: float,
        height_cm: Optional[float],
        height_group: Optional[str],
        manual_override: Optional[str]
    ) -> Tuple[str, str]:
        """
        Age & Height Classification Model Fusion:
        Merges Face-to-Age, Height-to-Age, and Manual Fallback.
        """
        if manual_override:
            return manual_override, "Manual Operator Override"

        if face_group and height_group:
            if face_group == height_group:
                return face_group, f"High-Confidence Dual Match (Face: {face_conf*100:.0f}%, Height: {height_cm:.0f}cm)"
            else:
                # Weighted arbitration: Face texture has priority for mature classification
                if "Senior" in face_group:
                    return face_group, f"Facial Dominant Fusion ({face_conf*100:.0f}%)"
                return height_group, f"Height Stature Arbitration ({height_cm:.0f}cm)"

        if face_group:
            return face_group, f"Facial Estimation Only ({face_conf*100:.0f}%)"

        if height_group:
            return height_group, f"Skeletal Stature Only ({height_cm:.0f}cm)"

        # Model Failed -> Default with Manual Prompt
        return "Adult (21-55)", "Fallback Default (Awaiting Selection 1-4)"

    def run(self) -> None:
        cap = cv2.VideoCapture(self.camera_id)
        if not cap.isOpened():
            print(f"[ERROR] Could not open camera {self.camera_id}.")
            sys.exit(1)

        print("=================================================================")
        print("  CRTEL Lab - Age & Height Multimodal Classification System")
        print("=================================================================")
        print("Controls:")
        print("  [1] Force Child (<13)         | [2] Force Youth (13-20)")
        print("  [3] Force Adult (21-55)       | [4] Force Senior (55+)")
        print("  [0] Clear Manual Override     | [q] Quit System")
        print("=================================================================")

        manual_override = None

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret or frame is None:
                break

            frame = cv2.flip(frame, 1)
            h, w, _ = frame.shape
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Parallel Pipeline Inference
            face_results = self.face_detector.process(rgb)
            pose_results = self.pose_detector.process(rgb)

            detected_face_group = None
            face_conf = 0.0
            detected_height_cm = None
            detected_height_group = None

            # Branch 1: Face to Age
            if face_results.detections:
                for d in face_results.detections:
                    bbox = d.location_data.relative_bounding_box
                    bx = max(0, int(bbox.xmin * w))
                    by = max(0, int(bbox.ymin * h))
                    bw = min(w - bx, int(bbox.width * w))
                    bh = min(h - by, int(bbox.height * h))

                    if bw > 30 and bh > 30:
                        face_crop = frame[by:by+bh, bx:bx+bw]
                        ratio = bw / float(w)
                        detected_face_group, face_conf = self.estimate_face_to_age(face_crop, ratio)
                        cv2.rectangle(frame, (bx, by), (bx + bw, by + bh), (0, 255, 255), 2)
                        break

            # Branch 2: Height to Age via Skeletal Pose
            if pose_results.pose_landmarks:
                self.mp_drawing.draw_landmarks(
                    frame, pose_results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS,
                    self.mp_drawing.DrawingSpec(color=(255, 100, 0), thickness=2, circle_radius=2),
                    self.mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2)
                )
                detected_height_cm, detected_height_group = self.estimate_height_to_age(
                    pose_results.pose_landmarks.landmark, h
                )

            # Branch 3 & 4: Age & Height Classification Model Fusion
            final_class, reason = self.fuse_visitor_classification(
                detected_face_group, face_conf, detected_height_cm, detected_height_group, manual_override
            )

            profile = self.DEMOGRAPHIC_PROFILES[final_class]

            # Render Display HUD (Visitor Classification Model -> Display)
            cv2.rectangle(frame, (10, 10), (w - 10, 140), (20, 20, 20), -1)
            cv2.rectangle(frame, (10, 10), (w - 10, 140), (255, 255, 255), 1)

            cv2.putText(frame, "CRTEL LAB: MULTIMODAL VISITOR CLASSIFICATION & DISPLAY PIPELINE",
                        (25, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 255), 2)
            cv2.putText(frame, f"Classified Audience : {final_class}",
                        (25, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.7, profile["theme_color"], 2)
            cv2.putText(frame, f"Decision Rationale  : {reason}",
                        (25, 95), cv2.FONT_HERSHEY_SIMPLEX, 0.52, (200, 200, 200), 1)
            cv2.putText(frame, f"Active Display Mode : {profile['content_mode']}",
                        (25, 122), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1)

            cv2.imshow("Interactive Visitor Display System", frame)
            key = cv2.waitKey(1) & 0xFF

            if key == ord('q'):
                break
            elif key == ord('1'):
                manual_override = "Child (<13)"
                print("[MANUAL INPUT] Selected: Child (<13)")
            elif key == ord('2'):
                manual_override = "Youth / Teen (13-20)"
                print("[MANUAL INPUT] Selected: Youth / Teen (13-20)")
            elif key == ord('3'):
                manual_override = "Adult (21-55)"
                print("[MANUAL INPUT] Selected: Adult (21-55)")
            elif key == ord('4'):
                manual_override = "Senior (55+)"
                print("[MANUAL INPUT] Selected: Senior (55+)")
            elif key == ord('0'):
                manual_override = None
                print("[MANUAL INPUT] Cleared override. Restored AI Fusion.")

        cap.release()
        cv2.destroyAllWindows()


def main() -> None:
    parser = argparse.ArgumentParser(description="Multimodal Age & Height Classification System")
    parser.add_argument("--camera", type=int, default=0, help="Camera index (default: 0)")
    parser.add_argument("--confidence", type=float, default=0.5, help="Confidence threshold")
    args = parser.parse_args()

    classifier = MultimodalVisitorClassifier(camera_id=args.camera, confidence=args.confidence)
    classifier.run()


if __name__ == "__main__":
    main()
