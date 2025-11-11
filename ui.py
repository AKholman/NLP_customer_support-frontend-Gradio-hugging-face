import gradio as gr
import requests

# -----------------------------
# Backend URL (Render deployment)
# -----------------------------
BACKEND_URL = "https://nlp-customer-support-sentence.onrender.com/search"

# -----------------------------
# Function to call backend API
# -----------------------------
def semantic_search(query, top_k):
    """
    Sends the query to the FastAPI backend and returns top text answers.
    """
    payload = {"query": query, "top_k": top_k}
    try:
        # Increase timeout to handle slower responses
        response = requests.post(BACKEND_URL, json=payload, timeout=120)
        
        if response.status_code == 200:
            data = response.json()
            # Backend should return actual answers text in "results_text"
            # If backend returns indices, replace this with text lookup
            return "\n\n".join(data["results"])
        else:
            return f"Error {response.status_code}: {response.text}"
        
    except requests.exceptions.RequestException as e:
        return f"Connection error: {e}"

# -----------------------------
# Gradio Interface
# -----------------------------
iface = gr.Interface(
    fn=semantic_search,
    inputs=[
        gr.Textbox(
            label="Enter your customer question",
            placeholder="Type your query here..."
        ),
        gr.Slider(
            1, 5, value=3, step=1, label="Top K Results"
        )
    ],
    outputs=gr.Textbox(label="Top Answers"),
    title="Customer Support Semantic Search",
    description="Enter a question to retrieve the most relevant customer support answers from the backend API."
)

# -----------------------------
# Launch
# -----------------------------
if __name__ == "__main__":
    # share=True is optional for temporary public link testing
    iface.launch()
