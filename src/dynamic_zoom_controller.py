"""
Multi-Scale Dynamic Zoom & Spatial Positioning Controller
=========================================================
Developed at Central Research & Training Laboratory (CRTEL), NCSM
Author: Arafat Ali Mondal

Description:
    Implements multi-scale digital magnification (2x to 12x) centered on
    detected human targets or custom Regions of Interest (ROI), maintaining
    calibrated aspect ratio tiles for large interactive display walls.
"""

from typing import Tuple
import argparse
import sys
import cv2
import numpy as np


class DynamicZoomController:
    """
    Manages multi-scale cropping, interpolation, and smooth zooming.
    """

    ZOOM_LEVELS = [1.0, 2.0, 3.0, 4.0, 5.0, 8.0, 12.0]

    def __init__(self, camera_id: int = 0) -> None:
        self.camera_id = camera_id
        self.current_zoom_index = 0

    @property
    def zoom_factor(self) -> float:
        return self.ZOOM_LEVELS[self.current_zoom_index]

    def cycle_zoom(self, direction: int = 1) -> float:
        """
        Cycle through zoom levels: direction=1 for zoom-in, -1 for zoom-out.
        """
        self.current_zoom_index = (self.current_zoom_index + direction) % len(self.ZOOM_LEVELS)
        return self.zoom_factor

    def apply_zoom(
        self,
        frame: np.ndarray,
        center_x: int,
        center_y: int
    ) -> np.ndarray:
        """
        Crop a sub-region centered at (center_x, center_y) and resize to full resolution.
        """
        factor = self.zoom_factor
        if factor <= 1.0:
            return frame

        h, w, _ = frame.shape
        crop_w = int(w / factor)
        crop_h = int(h / factor)

        # Calculate bounding box coordinates with clamping
        x1 = max(0, min(center_x - crop_w // 2, w - crop_w))
        y1 = max(0, min(center_y - crop_h // 2, h - crop_h))
        x2 = x1 + crop_w
        y2 = y1 + crop_h

        cropped = frame[y1:y2, x1:x2]
        return cv2.resize(cropped, (w, h), interpolation=cv2.INTER_LINEAR)

    def run(self) -> None:
        """
        Interactive demonstration loop.
        Controls:
          '+' or '=': Zoom In
          '-': Zoom Out
          'r': Reset Zoom to 1.0x
          Left Click on video window: Re-center Zoom
          'q': Quit
        """
        cap = cv2.VideoCapture(self.camera_id)
        if not cap.isOpened():
            print(f"[ERROR] Could not open camera {self.camera_id}.")
            sys.exit(1)

        center_x, center_y = None, None

        def on_mouse(event, x, y, flags, param):
            nonlocal center_x, center_y
            if event == cv2.EVENT_LBUTTONDOWN:
                center_x, center_y = x, y
                print(f"[INFO] New zoom center: ({center_x}, {center_y})")

        window_name = "CRTEL Lab - Dynamic Zoom Controller (Click to Center, +/- to Zoom)"
        cv2.namedWindow(window_name)
        cv2.setMouseCallback(window_name, on_mouse)

        print("[INFO] Controls: [+] Zoom In, [-] Zoom Out, [r] Reset, [q] Quit.")

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret or frame is None:
                break

            frame = cv2.flip(frame, 1)
            h, w, _ = frame.shape

            if center_x is None or center_y is None:
                center_x, center_y = w // 2, h // 2

            zoomed_frame = self.apply_zoom(frame, center_x, center_y)

            # Draw HUD overlay
            hud_text = f"Zoom: {self.zoom_factor:.1f}x | Center: ({center_x}, {center_y})"
            cv2.putText(zoomed_frame, hud_text, (20, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

            cv2.imshow(window_name, zoomed_frame)
            key = cv2.waitKey(1) & 0xFF

            if key == ord('q'):
                break
            elif key in (ord('+'), ord('=')):
                self.cycle_zoom(1)
            elif key in (ord('-'), ord('_')):
                self.cycle_zoom(-1)
            elif key == ord('r'):
                self.current_zoom_index = 0
                center_x, center_y = w // 2, h // 2

        cap.release()
        cv2.destroyAllWindows()


def main() -> None:
    parser = argparse.ArgumentParser(description="Multi-Scale Zoom Controller")
    parser.add_argument("--camera", type=int, default=0, help="Camera index")
    args = parser.parse_args()

    controller = DynamicZoomController(camera_id=args.camera)
    controller.run()


if __name__ == "__main__":
    main()

