import os
from typing import Dict, Any, List

# --- Meta trainer imports ---
import trainer_meta
conn = trainer_meta.init_db()

try:
    # Ultralytics YOLOv8 (install via: pip install ultralytics)
    from ultralytics import YOLO
    YOLO_AVAILABLE = True
except ImportError:
    YOLO_AVAILABLE = False

# Default model path (you can swap in your own trained weights)
DEFAULT_MODEL_PATH = r"C:\Users\jsmar\DeepSee\models\yolov8n.pt"

def load_detector(model_path: str = DEFAULT_MODEL_PATH):
    """
    Load YOLOv8 detector if available.
    Falls back to default weights if custom path is missing.
    Logs detector status to meta trainer.
    """
    if not YOLO_AVAILABLE:
        print("YOLOv8 not installed. Semantic detection will return placeholders.")
        trainer_meta.log_event(conn, None, "detector_unavailable", actor="object_detection", details="YOLOv8 not installed")
        return None

    if not os.path.exists(model_path):
        print(f"Model not found: {model_path}. Using default YOLOv8n weights.")
        trainer_meta.log_event(conn, None, "detector_model_missing", actor="object_detection", details=model_path)
        return YOLO("yolov8n.pt")

    trainer_meta.log_event(conn, None, "detector_load", actor="object_detection", details=model_path)
    return YOLO(model_path)
def detect_objects(image_path: str, model_path: str = DEFAULT_MODEL_PATH) -> Dict[str, Any]:
    """
    Run object detection on an image and return structured semantic results.
    Returns dict with keys: objects, faces, hands, ears, buildings, anomaly_flags, scene_consistency.
    """
    if not os.path.exists(image_path):
        trainer_meta.log_event(conn, None, "detect_objects_error", actor="object_detection", details="file not found")
        raise FileNotFoundError(f"Image not found: {image_path}")

    sha256 = trainer_meta.compute_sha256(image_path)
    phash = trainer_meta.compute_phash(image_path)
    trainer_meta.log_image(conn, sha256, phash, image_path)

    if not YOLO_AVAILABLE:
        trainer_meta.log_event(conn, sha256, "detect_objects_placeholder", actor="object_detection", details="YOLO unavailable")
        return {
            "objects": [],
            "faces": [],
            "hands": [],
            "ears": [],
            "buildings": [],
            "anomaly_flags": [],
            "scene_consistency": "unknown"
        }

    # Load detector
    model = load_detector(model_path)
    results = model(image_path)

    objects: List[Dict[str, Any]] = []
    faces, hands, ears, buildings = [], [], [], []
    anomaly_flags = []
    for r in results:
        for box in r.boxes:
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])
            label = model.names.get(cls_id, f"class_{cls_id}")
            bbox = box.xyxy[0].tolist()

            obj = {"label": label, "score": conf, "bbox": bbox}
            objects.append(obj)

            # Semantic grouping
            if "person" in label.lower():
                faces.append(obj)
            if "hand" in label.lower():
                hands.append(obj)
            if "ear" in label.lower():
                ears.append(obj)
            if "building" in label.lower() or "house" in label.lower():
                buildings.append(obj)

    # Example anomaly detection heuristic
    if len(hands) > 0 and any(o["score"] < 0.3 for o in hands):
        anomaly_flags.append("hand_anomaly")
    if len(faces) > 5:
        anomaly_flags.append("too_many_faces")

    scene_consistency = "consistent" if len(buildings) <= 2 else "inconsistent"
    results_dict = {
        "objects": objects,
        "faces": faces,
        "hands": hands,
        "ears": ears,
        "buildings": buildings,
        "anomaly_flags": anomaly_flags,
        "scene_consistency": scene_consistency
    }

    trainer_meta.log_event(
        conn,
        sha256,
        "detect_objects",
        actor="object_detection",
        details=(
            f"{image_path}:objects={len(objects)}, "
            f"faces={len(faces)}, hands={len(hands)}, "
            f"ears={len(ears)}, buildings={len(buildings)}, "
            f"anomalies={anomaly_flags}"
        )
    )

    return results_dict
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python scripts\\object_detection.py <image_path> [optional_model_path]")
        sys.exit(1)

    image_path = sys.argv[1]
    model_path = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_MODEL_PATH

    trainer_meta.log_event(conn, None, "script_entry", actor="object_detection", details="object_detection.py invoked")
    try:
        results = detect_objects(image_path, model_path=model_path)
        print("Semantic detection results:")
        for k, v in results.items():
            print(f"{k}: {v}")
        trainer_meta.log_event(
            conn,
            None,
            "script_exit",
            actor="object_detection",
            details=f"{image_path}:objects={len(results['objects'])}, anomalies={results['anomaly_flags']}"
        )
    except Exception as e:
        print(f"Fatal error: {e}")
        trainer_meta.log_event(conn, None, "script_exit_error", actor="object_detection", details=str(e))
        sys.exit(1)
