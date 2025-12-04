import gradio as gr
from deepsee_pipeline import run_pipeline

def classify_image(image):
    verdict, semantic, calibration = run_pipeline(image)

    # Format calibration nicely
    calib_display = {
        "Human %": round(calibration.get("human", 0.0) * 100, 2),
        "AI %": round(calibration.get("ai_generated", 0.0) * 100, 2),
        "Raw": calibration
    }

    # Format semantic cues
    semantic_display = {
        "Faces Detected": semantic.get("faces", []),
        "Anomaly Flags": semantic.get("anomaly_flags", [])
    }

    return verdict, calib_display, semantic_display

demo = gr.Interface(
    fn=classify_image,
    inputs=gr.Image(type="filepath", label="Upload Image"),
    outputs=[
        gr.Textbox(label="Final Verdict"),
        gr.JSON(label="Calibration Results"),
        gr.JSON(label="Semantic Analysis")
    ],
    title="DeepSee™ Cockpit",
    description="Privacy-first forensic classifier for human vs AI-generated images with calibrated probabilities"
)

if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=7860, share=False)
