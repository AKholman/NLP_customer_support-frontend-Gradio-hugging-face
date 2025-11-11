import gradio as gr
import requests

# --- Backend API endpoint (Render URL) ---
BACKEND_URL = "https://nlp-customer-support-sentence.onrender.com/search"

def semantic_search(query, top_k):
    """
    Sends a query to the FastAPI backend and returns top text answers.
    """
    if not query.strip():
        return "Please enter a question."

    payload = {"query": query, "top_k": int(top_k)}

    try:
        response = requests.post(BACKEND_URL, json=payload, timeout=30)
        if response.status_code == 200:
            data = response.json()
            # Expecting backend to return: {"results": ["answer1", "answer2", ...]}
            answers = data.get("results", [])
            if not answers:
                return "No relevant answers found."
            # Combine answers neatly for UI
            formatted = "\n\n".join([f"• {ans}" for ans in answers])
            return formatted
        else:
            return f"❌ Error {response.status_code}: {response.text}"
    except requests.exceptions.RequestException as e:
        return f"⚠️ Connection error: {e}"

# --- Build Gradio UI ---
iface = gr.Interface(
    fn=semantic_search,
    inputs=[
        gr.Textbox(label="💬 Enter your question", placeholder="e.g. How can I reset my password?"),
        gr.Slider(1, 5, value=3, step=1, label="Top K Results")
    ],
    outputs=gr.Textbox(label="🔍 Retrieved Answers", lines=8),
    title="Customer Support Semantic Search",
    description="Ask a customer support question and get the most relevant answers from real Twitter data.",
    theme="soft"
)

if __name__ == "__main__":
    iface.launch()
