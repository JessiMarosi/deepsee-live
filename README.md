# deepsee-live  
**DeepSee™ – Fully On-Device AI Content Detector**  
**No cloud • No data collection • Binary forensic verdicts**

Official repository and live cockpit for **DeepSee™** — the privacy-first, reproducible, audit-grade AI content classifier that runs 100% on-device (images, videos, audio).

[![Demo Video](https://img.shields.io/badge/▶️_Watch_Demo_on_YouTube-red?style=for-the-badge&logo=youtube)](https://youtu.be/ntOkek5MnxE)  
[![Launch Cockpit](https://img.shields.io/badge/Launch_Cockpit-1f1f1f?style=for-the-badge&logo=github)](https://github.com/JessiMarosi/deepsee-live/tree/main/cockpit)

---

## Demo & Proof of Operation

Watch the full GUI walkthrough and reproducible inference in action:

[Watch on YouTube →](https://youtu.be/ntOkek5MnxE)

Highlights:
- Real-time classification of AI-generated vs legitimate images
- Strict binary verdicts: `THIS IMAGE IS LIKELY AI` │ `THIS IMAGE IS LIKELY LEGITIMATE`
- Audit-grade logging with full reproducibility
- Zero data leaves the device

---

## Repository Structure

---

## Cockpit – Forensic Classification in Action

The `cockpit/` directory is the heart of DeepSee™:

| Feature                            | Implementation                                      |
|------------------------------------|------------------------------------------------------|
| On-device inference                | TensorFlow Lite + custom forensic feature extractors |
| Strict binary verdict logic        | Enforced in `deepsee_pipeline.py`                    |
| Audit-grade logging                | SQLite (`deepsee_trainer.db`) + CSV export            |
| Public GUI                         | Gradio app via `launch_gui.py`                       |
| Reproducible results               | Same seed, same model, same verdict — every time     |

### Example Verdicts (Real Runs)

| Input Image                              | Verdict                            | Confidence |
|------------------------------------------|------------------------------------|------------|
| ![AI Example](docs/proof_ai.jpg)         | **THIS IMAGE IS LIKELY AI**        | 98.61%     |
| ![Legitimate Example](docs/proof_legit.jpg) | **THIS IMAGE IS LIKELY LEGITIMATE**| 98.62%     |

Every verdict is logged with timestamp, hash, model version, and confidence — fully reproducible via CLI or GUI.

---

## Mission

To restore trust in digital media with **transparent, reproducible, and private** forensic classification — no cloud, no telemetry, no compromise.

Built from the ground up by **Jessica S. Marosi**, Founder & CEO of **ByteLock™**.

---

## Usage

```bash
# 1. Clone and enter repo
git clone https://github.com/JessiMarosi/deepsee-live.git
cd deepsee-live

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch the live cockpit (Gradio GUI)
python cockpit/launch_gui.py

Or explore the live demo directly:

https://deepsee.live (powered by this repo + GitHub Pages)

License

This reference implementation and cockpit are released under the MIT License — see LICENSE.

DeepSee™ and ByteLock™ are trademarks of ByteLock, Inc.
Commercial deployment, branding usage, or integration into products requires a separate license.

Made with zero trust in the cloud — and full trust in reproducibility.
© 2025 Jessica S. Marosi — All rights reserved.

