# Interactive Display System for Spatial Content Exploration
### Real-Time Human Detection, Dynamic ROI Tracking & Multi-Scale Zoom Controller

[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg?style=flat-square&logo=python)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.7%2B-5C3EE8.svg?style=flat-square&logo=opencv)](https://opencv.org/)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-Pose%20%26%20Face-00C4B4.svg?style=flat-square)](https://developers.google.com/mediapipe)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)
[![Institution](https://img.shields.io/badge/Institution-CRTEL%20%7C%20NCSM-darkgreen.svg?style=flat-square)](https://ncsm.gov.in/)

---

## 📌 Overview
This repository contains the official codebase and experimental artifacts developed at the **Central Research & Training Laboratory (CRTEL)**, **National Council of Science Museums (NCSM)**, Kolkata, India.

The project demonstrates an **Interactive Display System for Spatial Content Exploration in Museums**. It bridges edge computer vision with interactive exhibit hardware, utilizing real-time human pose estimation, custom Region of Interest (ROI) selection, dynamic multi-scale digital zoom (2x to 12x), and presence-activated multimedia triggering.

```
       [ Live Camera Feed ]
                 │
                 ▼
     [ Interactive ROI Gating ]
                 │
                 ▼
     [ MediaPipe Pose / Face ] ──► [ Spatial Position Coordinates ]
                 │                                │
                 ▼                                ▼
     [ Dynamic Multi-Scale Zoom ] ────► [ Event Trigger & Media Output ]
       (2x, 3x, 5x, 8x, 12x)             (Video / Audio Playback)
```

---

## 🌟 Key Features

1. **Interactive ROI Selection**:
   * Drag-and-drop bounding box selection to restrict computer vision processing to specific physical exhibit zones, minimizing false positives.
2. **Real-Time Human Pose Tracking**:
   * High-accuracy skeleton keypoint detection and bounding box computation powered by **MediaPipe Pose**.
3. **Multi-Scale Dynamic Zoom Engine**:
   * Smooth digital zoom transitions across calibrated factors (`2x`, `3x`, `4x`, `5x`, `8x`, `12x`) centered on visitor coordinates or interactive click targets.
4. **Presence-Activated Media Player**:
   * Automatically triggers interactive exhibit video playback, narrative commentary, and display transitions when a visitor steps into the active area.
5. **Hardware Benchmark Tool**:
   * Evaluates matrix multiplication and inference latency between CPU and GPU to optimize performance on compact museum display microcontrollers.

---

## 📂 Repository Structure

```text
CRTEL-Lab-Project-Demo/
├── src/                                  # Production & modular source code
│   ├── __init__.py
│   ├── human_detection_roi.py            # Main interactive ROI selection & human tracking
│   ├── dynamic_zoom_controller.py        # Multi-scale zoom & re-centering engine
│   ├── face_detection.py                 # Multi-person face detection module
│   ├── interactive_media_player.py       # Presence-triggered multimedia playback
│   └── benchmark_compute.py              # CPU vs GPU throughput benchmark
├── experiments/                          # Research experiments & calibration scripts
│   ├── posotion_fixed/                   # 12x zoom, 3x-8x ROI calibration, and position logs
│   ├── roi_variants/                     # Progressive ROI implementation prototypes
│   ├── video_trigger_tests/              # OpenCV and VLC multimedia triggering tests
│   ├── calibration_table.txt             # Empirical tile count vs zoom factor calibration
│   └── benchmark_cpu_gpu.py              # Raw compute throughput test
├── docs/                                 # Architectural specifications and diagrams
│   └── architecture.md
├── requirements.txt                      # Project dependencies
├── CITATION.cff                          # Academic citation metadata
├── LICENSE                               # MIT License
└── README.md
```

---

## 🚀 Getting Started

### 1. Prerequisites
* Python 3.8, 3.9, 3.10, or 3.11
* A standard USB webcam or integrated laptop camera

### 2. Installation
Clone the repository and install the dependencies:
```bash
git clone https://github.com/arafat678/CRTEL-Lab-Project-Demo.git
cd CRTEL-Lab-Project-Demo
pip install -r requirements.txt
```

---

## 💻 Usage

### 1. Human Detection with Interactive ROI Selection
Launch the interactive tracker. A window will open allowing you to draw a box on the active zone and press **SPACE**:
```bash
python src/human_detection_roi.py --camera 0 --confidence 0.5
```
*To run detection across the entire frame without manual ROI selection:*
```bash
python src/human_detection_roi.py --no-roi
```

### 2. Multi-Scale Dynamic Zoom Controller
Launch the zoom controller to test multi-tier magnification (`2x` to `12x`):
```bash
python src/dynamic_zoom_controller.py --camera 0
```
* **Left Click**: Set new zoom focal center.
* **`+` / `-`**: Zoom In / Zoom Out.
* **`r`**: Reset zoom to 1.0x.
* **`q`**: Quit.

### 3. Presence-Activated Media Trigger
Automatically play interactive content when a visitor is detected:
```bash
python src/interactive_media_player.py --video path/to/exhibit_video.mp4
```

### 4. Run Compute Benchmark
Test real-time inference latency on your hardware:
```bash
python src/benchmark_compute.py
```

---

## 📊 Empirical Zoom Calibration (CRTEL Lab Data)

Extracted from experimental lab trials on museum display tile matrices (`experiments/calibration_table.txt`):

| Optical / Digital Zoom | Calibrated Tile Units | Spatial Coverage |
| :---: | :---: | :---: |
| **2x** | 9 tiles | Broad Interactive Floor Area |
| **3x** | 11 tiles | Medium-Range Exhibit Focus |
| **4x** | 13 tiles | Focused Subject Tracking |
| **5x** | 11 tiles | Close-Up Feature Framing |
| **12x** | Variable | High-Precision Target Lock |

---

## 📝 Citation

If this research or codebase contributes to your academic work or exhibition design, please cite it as:

```bibtex
@software{mondal2024crtel,
  author       = {Mondal, Arafat Ali},
  title        = {Interactive Display System for Spatial Content Exploration: Real-Time Human Detection & ROI Tracking},
  year         = {2024},
  publisher    = {GitHub},
  journal      = {GitHub repository},
  howpublished = {\url{https://github.com/arafat678/CRTEL-Lab-Project-Demo}}
}
```

---

## 📜 License
This project is licensed under the [MIT License](LICENSE).
Developed for Central Research & Training Laboratory (CRTEL), National Council of Science Museums (NCSM).
