import os
import numpy as np
import tensorflow as tf
from typing import Tuple, List, Dict, Any

# --- Meta trainer imports ---
import trainer_meta
conn = trainer_meta.init_db()

# Default model path
DEFAULT_TFLITE_MODEL = r"C:\Users\jsmar\DeepSee\tflite\deepsee_mobilenetv2_dynamic.tflite"

# --- Feature vector construction ---
def build_feature_vector(feats: Dict[str, float], dists: Dict[str, float], semantic: Dict[str, Any]) -> np.ndarray:
    """
    Construct a 7-element feature vector for TFLite input:
    [has_exif, ela_score, edge_score, human_dist, ai_dist, face_score, anomaly_score]
    """
    has_exif = float(feats.get("has_exif", 0))
    ela_score = float(feats.get("ela_score", 0))
    edge_score = float(feats.get("edge_score", 0))
    human_dist = float(dists.get("human_distance", 0))
    ai_dist = float(dists.get("ai_distance", 0))

    face_score = 0.0
    if "faces" in semantic and semantic["faces"]:
        face_score = float(semantic["faces"][0].get("score", 0))

    anomaly_score = float(len(semantic.get("anomaly_flags", [])))

    vec = np.array([[has_exif, ela_score, edge_score, human_dist, ai_dist, face_score, anomaly_score]], dtype=np.float32)
    return vec
def load_tflite_model(model_path: str = DEFAULT_TFLITE_MODEL) -> tf.lite.Interpreter:
    """
    Load a TFLite model and allocate tensors.
    """
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"TFLite model not found: {model_path}")
    interpreter = tf.lite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()
    trainer_meta.log_event(conn, None, "tflite_model_load", actor="classify_tflite", details=model_path)
    return interpreter

def run_inference(interpreter: tf.lite.Interpreter, feature_vec: np.ndarray) -> np.ndarray:
    """
    Run inference on a feature vector using the provided TFLite interpreter.
    Returns the raw probability vector.
    """
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    expected_shape = tuple(input_details[0]["shape"])
    if feature_vec.shape != expected_shape:
        raise ValueError(f"Input shape mismatch: got {feature_vec.shape}, expected {expected_shape}")

    interpreter.set_tensor(input_details[0]["index"], feature_vec)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]["index"])
    return np.squeeze(output_data)

def predict_probs(feats: Dict[str, float], dists: Dict[str, float], semantic: Dict[str, Any],
                  model_path: str = DEFAULT_TFLITE_MODEL) -> Tuple[List[str], List[float], str, float, Dict[str, Any]]:
    """
    Predict probabilities using the TFLite model on extracted features.
    Returns:
      labels: list of class labels
      probs: list of probabilities
      top_label: highest-probability label
      top_score: confidence score
      semantic: passthrough dict for semantic features
    """
    interpreter = load_tflite_model(model_path)
    feature_vec = build_feature_vector(feats, dists, semantic)
    probs = run_inference(interpreter, feature_vec)

    labels = ["human", "ai_generated"]
    top_idx = int(np.argmax(probs))
    top_label = labels[top_idx]
    top_score = float(probs[top_idx])

    trainer_meta.log_event(conn, None, "tflite_inference", actor="classify_tflite", details=f"{top_label}:{top_score:.4f}")
    return labels, probs.tolist(), top_label, top_score, semantic
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python scripts\\classify_tflite.py <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]

    # For demo purposes, build placeholder features.
    # In production, these should come from object_detection.py or deepsee_pipeline.py.
    feats = {"has_exif": 1, "ela_score": 0.3, "edge_score": 0.5}
    dists = {"human_distance": 0.4, "ai_distance": 0.7}
    semantic = {"faces": [{"label": "person", "score": 0.9}], "anomaly_flags": []}

    trainer_meta.log_event(conn, None, "script_entry", actor="classify_tflite", details="classify_tflite.py invoked")
    try:
        labels, probs, top_label, top_score, semantic = predict_probs(feats, dists, semantic)
        print("Classification results:")
        print(f"Labels: {labels}")
        print(f"Probabilities: {probs}")
        print(f"Top label: {top_label} ({top_score:.4f})")
        print(f"Semantic: {semantic}")

        trainer_meta.log_event(
            conn,
            None,
            "script_exit",
            actor="classify_tflite",
            details=f"{image_path}:{top_label}:{top_score:.4f}"
        )
    except Exception as e:
        print(f"Fatal error: {e}")
        trainer_meta.log_event(conn, None, "script_exit_error", actor="classify_tflite", details=str(e))
        sys.exit(1)
