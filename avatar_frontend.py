import gradio as gr
from PIL import Image
import requests

styles = ["Enhance", "Anime", "Photographic", "Digital Art", "Comic Book", "Fantasy Art", "Line Art",
          "Analog Film", "Neon Punk", "Isometric","Low Poly", "Origami", "Modelling Compound", "Cinematic",
          "3D Model", "Pixel Art", "Tile Texture"]
with gr.Blocks() as demo:
    prompt = gr.Textbox(label="Enter a prompt")
    shape = gr.Dropdown(label="Choose a shape", choices=["circular", "square"])
    style = gr.Dropdown(label="Choose a style", choices=styles)
    generate = gr.Button("Generate")
    img = gr.Image(label="Generated Image/new profile picture")
    
    save = gr.Button("Change whatsapp profile picture")
    
    @gr.on(triggers=[generate.click], inputs=[prompt, shape, style],outputs=img)
    def generateAvatar(prompt, option="square", style="default"):
        if option == []:
            option = ""
        if style == []:
            style = ""
        else:
            style += " style"
        prompt=option+" avatar, "+prompt+" "+style
        
        url = "http://localhost:3000/generate-avatar"  # Adjust URL based on your setup
        
        response = requests.post(url, json={"data": prompt})
        response.raise_for_status()  # Raise an error for non-200 status codes
        data = response.json()
        # load image from filepath
        img = Image.open("avatar.png")
        return img

    @gr.on(triggers=[save.click], inputs=[img])
    def change(img):
        url = "http://localhost:3000/change-avatar"  # Adjust URL based on your setup

        response = requests.post(url, json={"data": "avatar.png"})
        response.raise_for_status()  # Raise an error for non-200 status codes

demo.launch(share=True)