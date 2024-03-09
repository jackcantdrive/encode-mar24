from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import gradio as gr
import os
import io
import warnings
from PIL import Image
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
import requests

CUSTOM_PATH = "/custom"
app = FastAPI()

HELLO_ROUTE = "/hello"
GOODBYE_ROUTE = "/goodbye"
iframe_dimensions = "height=300px width=1000px"

index_html = f'''
<h1> Whatsapp Tooling using stability AI </h1>
'''

@app.get("/", response_class=HTMLResponse)
def index():
    return index_html

# Our Host URL should not be prepended with "https" nor should it have a trailing slash.
os.environ['STABILITY_HOST'] = 'grpc.stability.ai:443'

# Sign up for an account at the following link to get an API Key.
# https://platform.stability.ai/

# Click on the following link once you have created an account to be taken to your API Key.
# https://platform.stability.ai/account/keys

# Paste your API Key below.

os.environ['STABILITY_KEY'] = 'sk-MReRjGpRVBA9tw9iClExKiv8AcoLaXk6ED3OymGBWhhU6pLD'

stability_api = client.StabilityInference(
    key=os.environ['STABILITY_KEY'], # API Key reference.
    verbose=True, # Print debug messages.
    engine="stable-diffusion-xl-1024-v1-0", # Set the engine to use for generation.
    # Check out the following link for a list of available engines: https://platform.stability.ai/docs/features/api-parameters#engine
)

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
        # Set up our initial generation parameters.
        answers = stability_api.generate(
            prompt=option+" avatar, "+prompt+" "+style+" style",
            seed=4253978046, # If a seed is provided, the resulting generated image will be deterministic.
                     # What this means is that as long as all generation parameters remain the same, you can always recall the same image simply by generating it again.
                     # Note: This isn't quite the case for Clip Guided generations, which we'll tackle in a future example notebook.
            steps=50, # Amount of inference steps performed on image generation. Defaults to 30. 
            cfg_scale=8.0, # Influences how strongly your generation is guided to match your prompt.
                   # Setting this value higher increases the strength in which it tries to match your prompt.
                   # Defaults to 7.0 if not specified.
            width=1024, # Generation width, defaults to 512 if not included.
            height=1024, # Generation height, defaults to 512 if not included.
            samples=1, # Number of images to generate, defaults to 1 if not included.
            sampler=generation.SAMPLER_K_DPMPP_2M # Choose which sampler we want to denoise our generation with.
                                                 # Defaults to k_dpmpp_2m if not specified. Clip Guidance only supports ancestral samplers.
                                                 # (Available Samplers: ddim, plms, k_euler, k_euler_ancestral, k_heun, k_dpm_2, k_dpm_2_ancestral, k_dpmpp_2s_ancestral, k_lms, k_dpmpp_2m, k_dpmpp_sde)
        )

    # Set up our warning to print to the console if the adult content classifier is tripped.
    # If adult content classifier is not tripped, save generated images.
        for resp in answers:
            for artifact in resp.artifacts:
                if artifact.finish_reason == generation.FILTER:
                    warnings.warn(
                    "Your request activated the API's safety filters and could not be processed."
                    "Please modify the prompt and try again.")
                if artifact.type == generation.ARTIFACT_IMAGE:
                    img = Image.open(io.BytesIO(artifact.binary))
                    return img
    
    @gr.on(triggers=[save.click], inputs=[img])
    def change(img):
        url = "http://localhost:3000/change-avatar"  # Adjust URL based on your setup
        
        img = Image.fromarray(img.astype("uint8"), "RGB")
        img.save("avatar.png")
        print("Image saved")
        response = requests.post(url, json={"data": "avatar.png"})
        response.raise_for_status()  # Raise an error for non-200 status codes

hello_app = demo

def process_text(text1, text2, text3):
  # Send data to Node.js backend
  url = "http://localhost:3000/sends-message"  # Adjust URL based on your setup
  response = requests.post(url, json={"number": text1, "message": text2, "additional": text3})
  response.raise_for_status()  # Raise an error for non-200 status codes
  data = response.json()
  return data["msg"]

interface = gr.Interface(
    fn=process_text,
    inputs=["text", "text", "text", gr.Image()],
    outputs="text",
    title="Process Two Texts (Node.js Backend)",
)

goodbye_app = interface


app = gr.mount_gradio_app(app, hello_app, path=HELLO_ROUTE)
app = gr.mount_gradio_app(app, goodbye_app, path=GOODBYE_ROUTE)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)