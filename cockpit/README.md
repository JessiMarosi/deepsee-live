# DeepSee Cockpit

The DeepSee Cockpit is the on‑device forensic classifier that powers privacy‑first detection of AI‑generated content.  
Unlike cloud‑based detectors, this pipeline runs locally, logs every step, and produces reproducible audit trails.

---

## Key Achievements

- Calibrated classification: Combines raw model probabilities with forensic features (EXIF, ELA, edge scores) and semantic cues (faces, anomalies).
- Audit‑grade logging: Every action is stored in SQLite (`deepsee_trainer.db`) for transparency and reproducibility.
- GUI integration: A Gradio cockpit (`launch_gui.py`) provides an interface with verdicts, calibration percentages, and semantic analysis.
- Error‑free pipeline: Patched shape mismatches, added `run_pipeline()` entrypoint, and validated end‑to‑end reproducibility.
- Privacy‑first design: No cloud calls, no data collection — all inference runs locally.

---

## Architecture

object_detection.py → classify_tflite.py → deepsee_pipeline.py (features) (probabilities) (calibration + verdict) ↓ trainer_meta.py (DB logging) ↓ launch_gui.py (Gradio cockpit)

---

## 🧪 Cockpit Demo: Human vs AI Image Classification

This screenshot shows the DeepSee™ cockpit in action, classifying an uploaded image with calibrated confidence:

![Cockpit Demo](../docs/cockpit_demo.png)

- **Final Verdict**: THIS IMAGE IS LIKELY LEGITIMATE
- **Confidence**: 98.62%
- **Semantic Analysis**: No anomalies detected

Verdict logic is enforced via `deepsee_pipeline.py`, ensuring only two outcomes:
- `"THIS IMAGE IS LIKELY AI"`
- `"THIS IMAGE IS LIKELY LEGITIMATE"`

All components run locally, log every step, and produce reproducible audit trails.

## Quickstart

1. Create a virtual environment:
   ```bash
   python -m venv DeepSeeEnv
   source DeepSeeEnv/bin/activate   # Linux/Mac
   DeepSeeEnv\Scripts\activate      # Windows
Install dependencies:

bash
pip install -r requirements.txt
Launch the cockpit GUI:

bash
python scripts/launch_gui.py
Upload an image and view:

Final Verdict

Calibration Results

Semantic Analysis

Example DB Log
text
('final_verdict', 'human_pct=66.67, ai_pct=33.33, exif=True, verdict=human')
('calibration', 'human=0.667, ai=0.333')
('script_entry', 'deepsee_pipeline.py invoked')
('script_exit', 'sample.jpg:verdict=human')
Notes
Models in tflite/ and models/ are placeholders; bring your own .tflite for full inference.

Logs and temp training data are excluded via .gitignore to keep the repo clean.
