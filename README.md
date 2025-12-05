# deepsee-live
Official landing page for DeepSee™ – the fully on-device AI content detector (images, videos, audio). No cloud. No data collection.

## 🎥 Demo Video

Watch DeepSee™ in action — cockpit verdicts, GUI walkthrough, and reproducible inference:

[▶️ LiveDemo.mp4](LiveDemo.mp4)

This demo showcases:
- Real-time classification of AI vs legitimate images
- Binary verdict enforcement (`LIKELY AI` / `LIKELY LEGITIMATE`)
- GUI interface with audit-grade logging and reproducible results

[▶️ Launch Cockpit](https://github.com/JessiMarosi/deepsee-live/tree/main/cockpit)

## Mission

DeepSee™ is designed to restore trust in digital content by offering reproducible, on-device forensic classification.  

Built by Jessica S. Marosi, Founder of ByteLock™, this cockpit enforces binary verdict logic, logs every decision, and operates without cloud dependencies — ensuring privacy, reproducibility, and audit-grade transparency.

## ✅ Cockpit Verdict Proof: Human vs AI Classification

DeepSee™ runs fully on-device, classifying images with calibrated confidence and semantic analysis — no cloud, no data collection. The cockpit enforces strict verdict logic: only two outcomes are possible.

## Verdict Logic

DeepSee™ enforces strict binary classification:
- `THIS IMAGE IS LIKELY AI`
- `THIS IMAGE IS LIKELY LEGITIMATE`

No fallback strings. No ambiguity. Every verdict is logged and reproducible.

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

## Cockpit: Forensic Classifier and Audit Trail

The `cockpit/` folder contains the operational pipeline behind DeepSee™, designed for audit‑grade AI content detection.

### Core Capabilities
- **Calibrated classification** using forensic features (EXIF, ELA, edge analysis) and semantic cues
- **Strict verdict logic** → only two possible outcomes:  
  - `THIS IMAGE IS LIKELY AI`  
  - `THIS IMAGE IS LIKELY LEGITIMATE`
- **Audit‑grade logging** to SQLite (`deepsee_trainer.db`) with reproducible decision trails
- **GUI interface** built with Gradio (`launch_gui.py`) for public‑facing demonstrations
- **Fully reproducible, on‑device inference** — no cloud dependencies, no data leakage

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

### Proof of Operation
DeepSee™ cockpit has been tested with both AI‑generated and legitimate images, producing consistent verdicts with >98% confidence.  
All results are logged to `decisions.csv` and reproducible via CLI or GUI.
ity, and recruiter contact, see `cockpit/README.md`
