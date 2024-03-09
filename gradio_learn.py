import requests
import gradio as gr
import os

def process_text(text1, text2):
  # Send data to Node.js backend
  url = "http://localhost:3000/sends-message"  # Adjust URL based on your setup
  response = requests.post(url, json={"number": text1, "message": text2})
  response.raise_for_status()  # Raise an error for non-200 status codes
  data = response.json()
  return data["msg"]

interface = gr.Interface(
    fn=process_text,
    inputs=["text", "text"],
    outputs="text",
    title="Process Two Texts (Node.js Backend)",
)

interface.launch()