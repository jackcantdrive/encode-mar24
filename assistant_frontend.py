import requests
import gradio as gr
import os

def process_text(recipient_number, message, goal):
  # Send data to Node.js backend
  url = "http://localhost:3000/sends-message"  # Adjust URL based on your setup
  response = requests.post(url, json={"number": recipient_number, "message": message, "additional": goal})
  response.raise_for_status()  # Raise an error for non-200 status codes
  data = response.json()
  return data["msg"]

interface = gr.Interface(
    fn=process_text,
    inputs=["text", "text", "text"],
    outputs="text",
    title="Send a message to someone using AI, and let AI communicate for you!",
)

interface.launch(share=True)