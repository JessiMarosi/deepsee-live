# deepsee-live
Official landing page for DeepSee™ – the fully on-device AI content detector (images, videos, audio). No cloud. No data collection.

[▶️ Launch Cockpit](https://github.com/JessiMarosi/deepsee-live/tree/main/cockpit)

## ✅ Cockpit Verdict Proof: Human vs AI Classification

DeepSee™ runs fully on-device, classifying images with calibrated confidence and semantic analysis — no cloud, no data collection. The cockpit enforces strict verdict logic: only two outcomes are possible.

### 🔍 Verdict Logic
- **THIS IMAGE IS LIKELY AI**
- **THIS IMAGE IS LIKELY LEGITIMATE**

## 🧪 Proof of Operation: Real Image Classification

These two images were run through the DeepSee™ cockpit to demonstrate forensic classification in action:

| Input Image | Final Verdict | Confidence |
|-------------|----------------|------------|
| ![Likely AI](docs/proof_ai.jpg) | THIS IMAGE IS LIKELY AI | 98.61% |
| ![Likely Legitimate](docs/proof_legit.jpg) | THIS IMAGE IS LIKELY LEGITIMATE | 98.62% |

Each image was processed using:
- `classify_tflite.py` for raw model inference
- `deepsee_pipeline.py` for verdict enforcement
- `launch_gui.py` for cockpit display

All results are logged to `decisions.csv` and reproducible via CLI or GUI.  
Verdict logic is strictly binary: only `"THIS IMAGE IS LIKELY AI"` or `"THIS IMAGE IS LIKELY LEGITIMATE"` are possible.

These images serve as public proof that DeepSee™ is operational, reproducible, and audit-grade.


Each image was processed using:
- `classify_tflite.py` for image-based inference
- `deepsee_pipeline.py` for verdict enforcement
- `launch_gui.py` for cockpit display

All results are logged to `decisions.csv` and can be reproduced via the CLI or the GUI.

---

This section proves that DeepSee™ delivers consistent, audit-grade verdicts with no fallback strings or ambiguous outputs. Recruiters and reviewers can verify the logic, trace the pipeline, and replicate the results locally.

# DeepSee

DeepSee is a privacy-first, fully on-device AI content detector for images, videos, and audio.  
No cloud. No data collection.

This repository powers the official landing page at [deepsee.live](https://deepsee.live)  
It also contains the full forensic cockpit for recruiters and reviewers.

---

## Cockpit: Forensic classifier and audit trail

The `cockpit/` folder contains the operational pipeline behind DeepSee:

- Calibrated classification using forensic features and semantic cues
- Audit-grade logging to SQLite (`deepsee_trainer.db`)
- GUI interface built with Gradio (`launch_gui.py`)
- Fully reproducible, on-device inference — no cloud dependencies

To explore the classifier, calibration logic, and GUI:  
→ [View cockpit README](https://github.com/JessiMarosi/deepsee-live/tree/main/cockpit)

---

## Author

Built by Jessi Marosi — Founder and Architect of DeepSee  
For technical documentation, reproducibility, and recruiter contact, see `cockpit/README.md`
