import gradio as gr
import requests

# Render backend URL
BACKEND_URL = "https://nlp-customer-support-sentence.onrender.com/search"

def semantic_search(query, top_k):
    payload = {"query": query, "top_k": top_k}
    try:
        response = requests.post(BACKEND_URL, json=payload, timeout=120)
        if response.status_code == 200:
            data = response.json()
            # Assuming backend now returns text answers in `data["results_text"]`
            return "\n\n".join(data["results_text"])
        else:
            return f"Error {response.status_code}: {response.text}"
    except requests.exceptions.RequestException as e:
        return f"Connection error: {e}"


# Gradio Interface
iface = gr.Interface(
    fn=semantic_search,
    inputs=[
        gr.Textbox(label="Enter your question", placeholder="Type your customer query here..."),
        gr.Slider(1, 5, value=3, step=1, label="Top K Results")
    ],
    outputs=gr.Textbox(label="Top Answers"),
    title="Customer Support Semantic Search",
    description="Enter a question to retrieve the most relevant customer support answers."
)

if __name__ == "__main__":
    iface.launch()
