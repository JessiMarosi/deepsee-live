# deepsee-live
Official landing page for DeepSee™ – the fully on-device AI content detector (images, videos, audio). No cloud. No data collection.

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
