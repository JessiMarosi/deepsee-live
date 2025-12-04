from typing import Tuple, Dict, Any
from classify_tflite import predict_probs
from detect_objects import detect_objects
from calibrate import calibrated_human_probability, final_verdict_from_calibration
from trainer_meta import log_event

def run_pipeline(image_path: str, model=None) -> Tuple[str, Dict[str, Any], Dict[str, float]]:
    """
    Run the full DeepSee pipeline on the given image.
    Returns final verdict, semantic analysis, and calibration results.
    """
    # Step 1: Run semantic detection
    semantic = detect_objects(image_path)

    # Step 2: Extract features and distances
    feats = semantic.get("features", [])
    dists = semantic.get("distances", [])

    # Defensive fallback if features/distances are missing
    if not feats or not dists:
        feats = [0.0] * 128
        dists = [0.0] * 128

    # Step 3: Run classifier with preloaded model
    labels, probs, top_label, top_score, semantic_out = predict_probs(feats, dists, semantic, model=model)

    # Step 4: Run calibration logic
    calibration = calibrated_human_probability(probs, semantic_out)
    verdict = final_verdict_from_calibration(calibration)

    # Step 5: Log the event
    log_event(image_path, verdict, calibration)

    return verdict, semantic_out, calibration
