import google.generativeai as genai
from google.generativeai.types import HarmBlockThreshold, HarmCategory
import gradio as gr
from PIL import Image, ImageDraw, ImageFont
import json

# Fetch bounding boxes and labels
async def get_bounding_boxes(prompt: str, image: str, api_key: str):
    system_prompt = """
You are a helpful assistant, who always responds with the bounding box and label with the explanation JSON based on the user input, and nothing else.
Your response can also include multiple bounding boxes and their labels in the list.
The values in the list should be integers.
Here are some example responses:
{
    "explanation": "User asked for the bounding box of the dragon, so I will provide the bounding box of the dragon.",
    "bounding_boxes": [
        {"label": "dragon", "box": [ymin, xmin, ymax, xmax]}
    ]
}
{
    "explanation": "User asked for the bounding box of the fruits which are red in color, so I will provide the bounding box of the Apple and the Tomato.",
    "bounding_boxes": [
        {"label": "apple", "box": [ymin, xmin, ymax, xmax]},
        {"label": "tomato", "box": [ymin, xmin, ymax, xmax]}
    ]
}
""".strip()
    
    prompt = f"Return the bounding boxes and labels of: {prompt}"

    messages = [
        {"role": "user", "parts": [prompt, image]},
    ]

    genai.configure(api_key=api_key)

    generation_config = {
        "temperature": 1,
        "max_output_tokens": 8192,
        "response_mime_type": "application/json",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        safety_settings={
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE
        },
        system_instruction=system_prompt
    )

    try:
        response = await model.generate_content_async(messages)
    except Exception as e:
        if "API key not valid" in str(e):
            raise gr.Error(
                "Invalid API key. Please provide a valid Gemini API key.")
        elif "rate limit" in str(e).lower():
            raise gr.Error("Rate limit exceeded for the API key.")
        else:
            raise gr.Error(f"Failed to generate content: {str(e)}")

    response_json = json.loads(response.text)

    explanation = response_json["explanation"]
    bounding_boxes = response_json["bounding_boxes"]

    return bounding_boxes, explanation

# Adjust bounding boxes based on image size
async def adjust_bounding_box(bounding_boxes, image):
    width, height = image.size
    adjusted_boxes = []
    for item in bounding_boxes:
        label = item["label"]
        ymin, xmin, ymax, xmax = [coord / 1000 for coord in item["box"]]
        xmin *= width
        xmax *= width
        ymin *= height
        ymax *= height
        adjusted_boxes.append({"label": label, "box": [xmin, ymin, xmax, ymax]})
    return adjusted_boxes

# Process the image and draw bounding boxes and labels
async def process_image(image, text, api_key):
    if not api_key:
        raise gr.Error("Please provide a Gemini API key.")

    # Open the image using PIL
    image = Image.open(image)

    # Call the async bounding box function
    bounding_boxes, explanation = await get_bounding_boxes(text, image, api_key)

    # Adjust the bounding box based on the image dimensions
    adjusted_boxes = await adjust_bounding_box(bounding_boxes, image)

    # Draw the bounding boxes and labels on the image
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default(size=20)
    
    for item in adjusted_boxes:
        box = item["box"]
        label = item["label"]
        draw.rectangle(box, outline="red", width=3)
        # Draw the label above the bounding box
        draw.text((box[0], box[1] - 25), label, fill="red", font=font)

    # Format adjusted boxes for display
    adjusted_boxes_str = "\n".join(f"{item['label']}: {item['box']}" for item in adjusted_boxes)

    return explanation, image, adjusted_boxes_str

# Gradio app
async def gradio_app(image, text, api_key):
    return await process_image(image, text, api_key)

# Launch the Gradio interface
iface = gr.Interface(
    fn=gradio_app,
    inputs=[
        gr.Image(type="filepath"),
        gr.Textbox(label="Object(s) to detect", value="person"),
        gr.Textbox(label="Your Gemini API Key", type="password")
    ],
    outputs=[
        gr.Textbox(label="Explanation"),
        gr.Image(type="pil", label="Output Image"),
        gr.Textbox(label="Coordinates of the detected objects")
    ],
    title="Gemini Object Detection ✨",
    description="Detect objects in images using the Gemini 1.5 Flash model.",
    allow_flagging="never"
)

iface.launch()
