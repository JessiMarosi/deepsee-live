deepsee-liveDeepSee™ – Fully On-Device AI Content Detector
No cloud • No data collection • Strict binary forensic verdictsOfficial repository and live cockpit for DeepSee™ — the privacy-first, reproducible, audit-grade classifier for images, videos, and audio. 100% on-device inference.Watch Demo Launch Cockpit Live Demo: deepsee.liveRepository Structuredeepsee-live/
├── cockpit/           # Live GUI, pipeline, verdict engine (launch_gui.py)
├── Configs/           # Thresholds, verdict templates, inference settings
├── Diagrams/          # Architecture & on-device flow diagrams
├── Evidence/          # Sample inputs + reproducible reports
├── Images/            # Logos, screenshots, demo assets
├── Pages/             # Source for GitHub Pages landing
├── Scripts/           # classify_tflite.py, deepsee_pipeline.py, etc.
├── docs/              # Proof images, detailed forensic reports
├── index.html         # Public site → https://deepsee.live
├── requirements.txt   # Python dependencies
├── CNAME              # Custom domain
├── LICENSE            # MIT
└── README.mdCockpit FeaturesFeature
Implementation
On-device inference
TFLite + custom forensic extractors
Binary verdicts only
Enforced in deepsee_pipeline.py
Audit-grade logging
SQLite + CSV (hash, timestamp, confidence)
Public GUI
Gradio (cockpit/launch_gui.py)
100% reproducible
Fixed seed + version-locked model

Real ResultsImage
Verdict
Confidence
AI
THIS IMAGE IS LIKELY AI
98.61%
Legit
THIS IMAGE IS LIKELY LEGITIMATE
98.62%

Quick Startbash

git clone https://github.com/JessiMarosi/deepsee-live.git
cd deepsee-live
pip install -r requirements.txt
python cockpit/launch_gui.py

Or just visit the live demo: https://deepsee.liveMissionRestore trust in digital media with transparent, private, and fully reproducible AI detection.Created by Jessica S. Marosi • Founder & CEO, ByteLock™License & TrademarksCode & cockpit: MIT License (see LICENSE)  
DeepSee™ and ByteLock™ are trademarks of ByteLock, Inc.  
Commercial use or branding requires a separate license.

© 2025 Jessica S. Marosi. All rights reserved.

