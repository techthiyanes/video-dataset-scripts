from transformers import AutoModelForImageClassification, AutoImageProcessor
import torch

MODEL_ID = "Falconsai/nsfw_image_detection"

MODEL, PROCESSOR = None, None


def load_nsfw(device):
    global MODEL, PROCESSOR
    MODEL = AutoModelForImageClassification.from_pretrained(MODEL_ID).eval().to(device)
    PROCESSOR = AutoImageProcessor.from_pretrained(MODEL_ID)


@torch.no_grad()
def run_nsfw(image):
    if not isinstance(image, list):
        image = [image]
    inputs = PROCESSOR(images=image, return_tensors="pt").to(MODEL.device)
    outputs = MODEL(**inputs).logits
    predicted_labels = outputs.argmax(-1)
    return [MODEL.config.id2label[p.cpu().item()] for p in predicted_labels]
