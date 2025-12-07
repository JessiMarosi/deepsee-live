# deepsee-live
**DeepSee™ – Fully On-Device AI Content Detector**  
**No cloud • No data collection • Strict binary forensic verdicts**

Official repository and live cockpit for **DeepSee™** — privacy-first, reproducible, audit-grade AI content classifier (images, videos, audio). 100% on-device.

[![Watch Demo](https://img.shields.io/badge/Watch_Demo-FF0000?style=for-the-badge&logo=youtube)](https://youtu.be/ntOkek5MnxE)
[![Launch Cockpit](https://img.shields.io/badge/Launch_Cockpit-000000?style=for-the-badge&logo=github)](https://github.com/JessiMarosi/deepsee-live/tree/main/cockpit)
[![Live Site](https://img.shields.io/badge/deepsee.live-0066FF?style=for-the-badge)](https://deepsee.live)

## Repository Structure

deepsee-live/
├── cockpit/           # Live GUI, pipeline, verdict engine (launch_gui.py)
├── Configs/           # Thresholds, verdict templates, inference settings
├── Diagrams/          # Architecture & on-device processing flow
├── Evidence/          # Sample inputs + reproducible reports
├── Images/            # Logos, screenshots, demo assets
├── Pages/             # Source for GitHub Pages landing page
├── Scripts/           # classify_tflite.py, deepsee_pipeline.py, etc.
├── docs/              # Proof images and detailed forensic reports
├── index.html         # Public site → https://deepsee.live
├── requirements.txt   # Python dependencies
├── CNAME              # Custom domain
├── LICENSE            # MIT License
└── README.md

## Cockpit Features

| Feature                   | Implementation                                      |
|---------------------------|-----------------------------------------------------|
| On-device inference       | TensorFlow Lite + forensic feature extractors       |
| Binary verdicts only      | Enforced in `deepsee_pipeline.py`                   |
| Audit-grade logging       | SQLite + CSV (hash, timestamp, confidence)          |
| Public GUI                | Gradio (`cockpit/launch_gui.py`)                    |
| 100% reproducible         | Fixed seed + version-locked model                   |

### Real Results

| Image                          | Verdict                           | Confidence |
|-------------------------------|-----------------------------------|------------|
| ![AI](docs/proof_ai.jpg)      | **THIS IMAGE IS LIKELY AI**       | 98.61%     |
| ![Legit](docs/proof_legit.jpg)| **THIS IMAGE IS LIKELY LEGITIMATE**| 98.62%     |

## Quick Start
```bash
git clone https://github.com/JessiMarosi/deepsee-live.git
cd deepsee-live
pip install -r requirements.txt
python cockpit/launch_gui.py

Or visit the live demo instantly → https://deepsee.liveMissionRestore trust in digital media with transparent, private, and fully reproducible forensic AI detection.Created by Jessica S. Marosi · Founder & CEO, ByteLock™LicenseMIT License (see LICENSE)
DeepSee™ and ByteLock™ are trademarks of ByteLock, Inc. Commercial use requires a separate license.© 2025 Jessica S. Marosi. All rights reserved.

