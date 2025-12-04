import numpy as np
from typing import Dict, Any, List, Tuple

# --- Meta trainer imports ---
import trainer_meta
conn = trainer_meta.init_db()

def calibrated_human_probability(
    labels: List[str],
    probs: List[float],
    feats: Dict[str, Any],
    dists: Dict[str, Any],
    semantic: Dict[str, Any] = None
) -> Dict[str, float]:
    """
    Combine classifier probabilities, forensic features, and semantic cues
    into calibrated human vs AI probabilities.
    Returns dict with keys: "human", "ai_generated".
    """
    human_score = float(probs[labels.index("human")]) if "human" in labels else 0.0
    ai_score = float(probs[labels.index("ai_generated")]) if "ai_generated" in labels else 0.0

    # Adjustments based on forensic features
    if feats.get("has_exif", 0) == 1:
        human_score += 0.1
    if feats.get("ela_score", 0) > 0.5:
        ai_score += 0.1
    if feats.get("edge_score", 0) < 0.2:
        ai_score += 0.05

    # Adjustments based on baseline distances
    try:
        if float(dists.get("human_distance", 1.0)) < 0.5:
            human_score += 0.05
        if float(dists.get("ai_distance", 1.0)) < 0.5:
            ai_score += 0.05
    except Exception:
        pass
    # Adjustments based on semantic cues (from object_detection)
    if semantic:
        if semantic.get("faces") and len(semantic["faces"]) > 0:
            human_score += 0.05
        if semantic.get("anomaly_flags"):
            ai_score += 0.05

    # Normalize
    total = human_score + ai_score
    if total <= 0:
        return {"human": 0.5, "ai_generated": 0.5}

    human_prob = human_score / total
    ai_prob = ai_score / total

    trainer_meta.log_event(conn, None, "calibration", actor="deepsee_pipeline",
                           details=f"human={human_prob:.4f}, ai={ai_prob:.4f}")

    return {"human": human_prob, "ai_generated": ai_prob}


def final_verdict_from_calibration(calib: Dict[str, float], feats: Dict[str, Any]) -> str:
    """
    Decide a final verdict string based on calibrated probabilities and forensic features.
    Returns one of: "human", "ai_generated", "likely_not_ai", "likely_ai", "inconclusive".
    """
    human_pct = round(calib.get("human", 0.0) * 100, 2)
    ai_pct = round(calib.get("ai_generated", 0.0) * 100, 2)
    has_exif = int(feats.get("has_exif", 0)) == 1

    if has_exif and human_pct >= 90:
        verdict = "likely_not_ai"
    elif ai_pct >= 90:
        verdict = "likely_ai"
    elif human_pct >= 75 and has_exif:
        verdict = "likely_not_ai"
    elif ai_pct >= 75:
        verdict = "likely_ai"
    elif human_pct > ai_pct and human_pct >= 60:
        verdict = "human"
    elif ai_pct > human_pct and ai_pct >= 60:
        verdict = "ai_generated"
    else:
        verdict = "inconclusive"

    trainer_meta.log_event(
        conn,
        None,
        "final_verdict",
        actor="deepsee_pipeline",
        details=f"human_pct={human_pct}, ai_pct={ai_pct}, exif={has_exif}, verdict={verdict}"
    )

    return verdict
def run_pipeline(image_path: str) -> Tuple[str, Dict[str, Any], Dict[str, float]]:
    """
    Unified entrypoint for GUI: runs detection, classification, and calibration.
    Returns verdict, semantic, calibration dict.
    """
    from object_detection import detect_objects
    from classify_tflite import predict_probs

    # Run detection
    feats, dists, semantic = detect_objects(image_path)

    # Run classifier
    labels, probs, top_label, top_score, semantic = predict_probs(feats, dists, semantic)

    # Calibrate
    calib = calibrated_human_probability(labels, probs, feats, dists, semantic=semantic)

    # Verdict
    verdict = final_verdict_from_calibration(calib, feats)

    return verdict, semantic, calib


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python scripts\\deepsee_pipeline.py <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]
    trainer_meta.log_event(conn, None, "script_entry", actor="deepsee_pipeline", details="deepsee_pipeline.py invoked")

    try:
        # Example standalone test: simulate classifier + forensic features
        labels = ["human", "ai_generated"]
        probs = [0.6, 0.4]
        feats = {"has_exif": 1, "ela_score": 0.3, "edge_score": 0.5}
        dists = {"human_distance": 0.4, "ai_distance": 0.7}
        semantic = {"faces": [{"label": "person", "score": 0.9}], "anomaly_flags": []}

        calib = calibrated_human_probability(labels, probs, feats, dists, semantic=semantic)
        verdict = final_verdict_from_calibration(calib, feats)

        print("Calibration results:", calib)
        print("Final verdict:", verdict)

        trainer_meta.log_event(conn, None, "script_exit", actor="deepsee_pipeline",
                               details=f"{image_path}:verdict={verdict}")
    except Exception as e:
        print(f"Fatal error: {e}")
        trainer_meta.log_event(conn, None, "script_exit_error", actor="deepsee_pipeline", details=str(e))
        sys.exit(1)
