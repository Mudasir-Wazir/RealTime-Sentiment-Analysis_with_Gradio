import gradio as gr
from transformers import pipeline

# Load a specific, lightweight model for reproducibility
sentiment_analyzer = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english",
)


def analyze_sentiment(text: str):
    """Return class probabilities for POSITIVE/NEGATIVE.

    Gradio's Label component accepts a mapping of {label: score}.
    """
    if not text or not text.strip():
        return {"Provide some text to analyze": 1.0}

    result = sentiment_analyzer(text)[0]
    label = result["label"]
    score = float(result["score"])  # ensure plain float

    # Convert single prediction to a 2-class distribution for nicer UI
    if label.upper() == "POSITIVE":
        return {"POSITIVE": score, "NEGATIVE": 1.0 - score}
    else:
        return {"NEGATIVE": score, "POSITIVE": 1.0 - score}


examples = [
    ["I absolutely loved this movie!"],
    ["This was a terrible experience."],
    ["It's fine, not great but not awful either."],
]


iface = gr.Interface(
    fn=analyze_sentiment,
    inputs=gr.Textbox(lines=3, placeholder="Enter a sentence here..."),
    outputs=gr.Label(num_top_classes=2),
    title="Sentiment Analysis Bot",
    description=(
        "Type in a sentence and see if the model predicts POSITIVE or NEGATIVE.\n"
        "Built with Gradio and Hugging Face Transformers."
    ),
    examples=examples,
)

# Enable request queue for smoother concurrency
iface.queue().launch()