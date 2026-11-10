# System Architecture & Technical Specifications

## 1. Overview
The **CRTEL Lab Interactive Spatial Display System** is engineered to enable touchless, presence-aware multimedia exploration in public exhibitions and museum galleries. It tracks visitor entry, dynamically frames Regions of Interest (ROI), computes position coordinates, and triggers synchronized multimedia responses.

```
       [ Live Optical Video Stream ]
                     │
                     ▼
       ┌───────────────────────────┐
       │     Frame Preprocessing   │ (Resolution, Mirroring, Color Conversion)
       └─────────────┬─────────────┘
                     │
       ┌─────────────┴─────────────┐
       ▼                           ▼
┌──────────────┐            ┌──────────────┐
│  Static ROI  │            │  Dynamic ROI │
│  Selection   │            │  Estimation  │
└──────┬───────┘            └──────┬───────┘
       │                           │
       └─────────────┬─────────────┘
                     ▼
       ┌───────────────────────────┐
       │   MediaPipe Pose Pipeline │ (Skeletal Keypoints, Coordinate Extraction)
       └─────────────┬─────────────┘
                     │
                     ▼
       ┌───────────────────────────┐
       │ Multi-Scale Zoom Engine   │ (2x, 3x, 4x, 5x, 8x, 12x Tile Calibration)
       └─────────────┬─────────────┘
                     │
                     ▼
       ┌───────────────────────────┐
       │ Interactive Trigger Core  │ (Content Exploration, Video / Audio playback)
       └───────────────────────────┘
```

## 2. Key Modules
- **`src/human_detection_roi.py`**: Interactively selects active zones and monitors visitor ingress/egress.
- **`src/dynamic_zoom_controller.py`**: Smooth digital cropping and optical centering without aspect ratio distortion.
- **`src/face_detection.py`**: Rapid visitor count and engagement estimation.
- **`src/interactive_media_player.py`**: Event-driven multimedia orchestrator.
- **`src/benchmark_compute.py`**: Edge inference latency analyzer.

