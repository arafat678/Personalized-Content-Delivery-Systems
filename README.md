# Interactive Display System for Spatial Content Exploration
### Real-Time Human Detection, Dynamic ROI Tracking & AI-Based Personalized Content Delivery

[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg?style=flat-square&logo=python)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.7%2B-5C3EE8.svg?style=flat-square&logo=opencv)](https://opencv.org/)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-Pose%20%26%20Face-00C4B4.svg?style=flat-square)](https://developers.google.com/mediapipe)
[![Published in](https://img.shields.io/badge/Book%20Chapter-CRC%20Press%20%7C%20Taylor%20%26%20Francis-red.svg?style=flat-square)](https://www.routledge.com/)
[![ISBN](https://img.shields.io/badge/ISBN-9781041117636-blue.svg?style=flat-square)](https://www.routledge.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)
[![Institution](https://img.shields.io/badge/Institution-CRTEL%20%7C%20NCSM-darkgreen.svg?style=flat-square)](https://ncsm.gov.in/)

---

## 📌 Associated Research Publication

This codebase represents the engineering realization and experimental framework behind the published book chapter:

> **Chapter Title**: *Personalized Content Delivery Systems: An AI Based Age Estimation Approach*  
> **Book**: *Emerging Trends in Electrical and Computer Technologies (1st Edition)*  
> **Publisher**: **CRC Press (Taylor & Francis Group)**  
> **Publication Date**: July 12, 2026  
> **Contributors**: **Arafat Ali Mondal** *(Methodology, Writing - original draft)*, Arnab Chatterjee, Shatadal Ghosh, Manash Bagchi  
> **ISBN**: `9781041117636`  
> **Laboratory**: Central Research & Training Laboratory (CRTEL), National Council of Science Museums (NCSM), Kolkata, India  

---

## 📖 Overview
Developed at the **Central Research & Training Laboratory (CRTEL)**, **National Council of Science Museums (NCSM)**, this system bridges edge computer vision with smart museum exhibition hardware. It provides touchless, presence-aware spatial exploration through:
* **Real-time human pose estimation and bounding tracking**
* **Interactive Region of Interest (ROI) selection**
* **Facial feature analysis for demographic age-group estimation**
* **Dynamic content personalization based on audience profile**
* **Multi-scale digital zoom magnification (`2x` to `12x`)**

```
       [ Live Optical Video Feed ]
                    │
                    ▼
       ┌───────────────────────────┐
       │   Spatial ROI Filtering   │
       └────────────┬──────────────┘
                    │
       ┌────────────┴──────────────┐
       ▼                           ▼
┌──────────────┐            ┌──────────────┐
│  MediaPipe   │            │ AI Facial    │
│  Human Pose  │            │ Age Analysis │
└──────┬───────┘            └──────┬───────┘
       │                           │
       ▼                           ▼
[ Spatial Coordinates ]     [ Demographic Profile ]
(Visitor Position)          (Child / Youth / Adult / Senior)
       │                           │
       └────────────┬──────────────┘
                    ▼
       ┌───────────────────────────┐
       │ Personalized Content Core │
       │ Dynamic Media & Zooming   │
       └───────────────────────────┘
```

---

## 🌟 Key Features

1. **AI-Based Age Estimation & Content Personalization**:
   * Analyzes facial morphology and anthropometric ratios to classify visitors into audience demographics (`Child <13`, `Youth 13-25`, `Adult 26-55`, `Senior 55+`), dynamically streaming age-appropriate narrative styles and visual themes.
2. **Interactive ROI Selection**:
   * Drag-and-drop bounding box selection to restrict computer vision processing to specific physical exhibit zones, minimizing false positives.
3. **Real-Time Human Pose Tracking**:
   * High-accuracy skeleton keypoint detection and bounding box computation powered by **MediaPipe Pose**.
4. **Multi-Scale Dynamic Zoom Engine**:
   * Smooth digital zoom transitions across calibrated factors (`2x`, `3x`, `4x`, `5x`, `8x`, `12x`) centered on visitor coordinates or interactive click targets.
5. **Presence-Activated Media Player**:
   * Automatically triggers interactive exhibit video playback, narrative commentary, and display transitions when a visitor steps into the active area.
6. **Hardware Acceleration Benchmark**:
   * Evaluates matrix throughput between CPU (NumPy/BLAS) and GPU (TensorFlow) for compact museum display microcontrollers.

---

## 📂 Repository Structure

```text
CRTEL-Lab-Project-Demo/
├── src/                                  # Production & modular source code
│   ├── __init__.py
│   ├── age_estimation_content_delivery.py# AI age estimation & content personalization
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
```bash
git clone https://github.com/arafat678/CRTEL-Lab-Project-Demo.git
cd CRTEL-Lab-Project-Demo
pip install -r requirements.txt
```

---

## 💻 Usage

### 1. AI Age Estimation & Content Personalization (Published Chapter Method)
Run the real-time demographic adaptation engine:
```bash
python src/age_estimation_content_delivery.py --camera 0
```

### 2. Human Detection with Interactive ROI Selection
Launch the interactive tracker. A window opens allowing you to drag a box over the active exhibit zone and press **SPACE**:
```bash
python src/human_detection_roi.py --camera 0 --confidence 0.5
```
*To run detection across the entire frame without manual ROI selection:*
```bash
python src/human_detection_roi.py --no-roi
```

### 3. Multi-Scale Dynamic Zoom Controller
Launch the zoom controller to test multi-tier magnification (`2x` to `12x`):
```bash
python src/dynamic_zoom_controller.py --camera 0
```
* **Left Click**: Set new zoom focal center.
* **`+` / `-`**: Zoom In / Zoom Out.
* **`r`**: Reset zoom to 1.0x.
* **`q`**: Quit.

### 4. Presence-Activated Media Trigger
Automatically play interactive content when a visitor is detected:
```bash
python src/interactive_media_player.py --video path/to/exhibit_video.mp4
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

### Book Chapter Citation (IEEE Format)
```text
A. A. Mondal, A. Chatterjee, S. Ghosh, and M. Bagchi, "Personalized Content Delivery Systems: An AI Based Age Estimation Approach," in Emerging Trends in Electrical and Computer Technologies, 1st ed., Boca Raton, FL, USA: CRC Press, 2026. ISBN: 9781041117636.
```

### BibTeX
```bibtex
@incollection{mondal2026personalized,
  author    = {Mondal, Arafat Ali and Chatterjee, Arnab and Ghosh, Shatadal and Bagchi, Manash},
  title     = {Personalized Content Delivery Systems: An AI Based Age Estimation Approach},
  booktitle = {Emerging Trends in Electrical and Computer Technologies},
  edition   = {1st},
  publisher = {CRC Press (Taylor \& Francis Group)},
  year      = {2026},
  month     = {July},
  isbn      = {9781041117636}
}
```

---

## 📜 License
This project is licensed under the [MIT License](LICENSE).  
Developed at Central Research & Training Laboratory (CRTEL), National Council of Science Museums (NCSM).
