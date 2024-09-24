# Gemini Object Detection ✨

Gemini Object Detection is an AI-powered tool that leverages Google's Gemini 1.5 Flash models Image processing capabilities to identify objects within images. Upload an image, specify the objects you want to detect, and receive accurate bounding boxes and labels, all powered by the Gemini API.

![Object Detection](https://raw.githubusercontent.com/sxqib/gemini-object-detection/main/demo.gif)

## Features

- **Object Detection**: Identify and label multiple objects in an image with precise bounding boxes.
- **AI-powered**: Uses Gemini API for object detection with detailed bounding box coordinates.
- **Customizable Input**: Detect any objects you specify in the input text.
- **Bounding Box Adjustments**: Automatically adjusts bounding boxes based on image dimensions.
- **Image Annotation**: Annotates the image with bounding boxes and labels.

## Try It Out on Hugging Face
[![Open in HuggingFace Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces/saq1b/gemini-object-detection)

## How It Works

1. **Input**: Upload an image and describe the objects you want to detect (e.g., "cat," "car").
2. **AI Processing**:
   - The Gemini 1.5 Flash model generates bounding boxes and labels for the objects.
   - Bounding boxes are adjusted to fit the dimensions of the image.
3. **Output**: The tool provides:
   - A labeled image with bounding boxes.
   - Explanation and coordinates of the detected objects.

## Customization

- **Objects to Detect**: You can specify any objects to detect in your input text.
- **Bounding Box Adjustments**: Bounding boxes are automatically scaled based on the image resolution.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/sxqib/gemini-object-detection.git
   cd gemini-object-detection
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

1. Run the Gradio app:
   ```bash
   python app.py
   ```

## Acknowledgements

- **Google Gemini API** for powering the object detection.
- **Pillow (PIL)** for image processing and annotation.
- **Gradio** for the easy-to-use web interface.
