import os, io
from google.cloud import vision
from google.cloud.vision import types 

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"fine-citadel-256305-268fe6ec9dd9.json"

client = vision.ImageAnnotatorClient()

def detect_labels(path):
    """Detects labels in the file."""
    from google.cloud import vision
    import io
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.label_detection(image=image)
    labels = response.label_annotations
    print('Labels:')

    for label in labels:
        print(label.description)