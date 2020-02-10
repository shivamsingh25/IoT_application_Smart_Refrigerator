import argparse
import io
import os

# os.system('export GOOGLE_APPLICATION_CREDENTIALS="/home/shivam/Desktop/IoT/Google Cloud Vision AI/fine-citadel-256305-268fe6ec9dd9.json"');
# export GOOGLE_APPLICATION_CREDENTIALS="/home/shivam/Desktop/IoT/Google Cloud Vision AI/fine-citadel-256305-268fe6ec9dd9.json"

from google.cloud import vision
from google.cloud.vision import types

from Adafruit_IO import Client, Data
aio = Client('shivamsingh25', '67f3f8f5a101487f977605d1be16f5c1')

contents = aio.feeds('contents')

items = [None] * 10
count = 0

def annotate(path):
    """Returns web annotations given the path to an image."""
    client = vision.ImageAnnotatorClient()

    if path.startswith('http') or path.startswith('gs:'):
        image = types.Image()
        image.source.image_uri = path

    else:
        with io.open(path, 'rb') as image_file:
            content = image_file.read()

        image = types.Image(content=content)

    web_detection = client.web_detection(image=image).web_detection

    return web_detection


def report(annotations):
    """Prints detected features in the provided web annotations."""
    if annotations.pages_with_matching_images:
        print('\n{} Pages with matching images retrieved'.format(
            len(annotations.pages_with_matching_images)))

        for page in annotations.pages_with_matching_images:
            print('Url   : {}'.format(page.url))

    if annotations.full_matching_images:
        print('\n{} Full Matches found: '.format(
              len(annotations.full_matching_images)))

        for image in annotations.full_matching_images:
            print('Url  : {}'.format(image.url))

    if annotations.partial_matching_images:
        print('\n{} Partial Matches found: '.format(
              len(annotations.partial_matching_images)))

        for image in annotations.partial_matching_images:
            print('Url  : {}'.format(image.url))

    if annotations.web_entities:
        print('\n{} Web entities found: '.format(
              len(annotations.web_entities)))
        count = 0
        for entity in annotations.web_entities:
            print('Score      : {}'.format(entity.score))
            print('Description: {}'.format(entity.description))
            items[count] = '{}'.format(entity.description)
            count += 1

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    path_help = str('The image to detect, can be web URI, '
                    'Google Cloud Storage, or path to local file.')
    parser.add_argument('image_url', help=path_help)
    args = parser.parse_args()

    report(annotate(args.image_url))
    print(items)
    print('\n\n--> Welcome to Smart Refrigerator, \nPlease help me know what you just kept in the refrigerator from the following (auto-detected):')
    count1 = 0
    for i in items:
        print(count1+1)
        print(items[count1])
        count1 += 1
    print(count1+1)
    print('Other (User Entry)')
    userChoice = input('\n\n--> Enter your choice: ')
    if(userChoice == count1+1):
        userEntry = ""
        userEntry = raw_input('\n\n--> Enter the item you just kept in the refrigerator: ')
        aio.send_data(contents.key, userEntry)
        os.system('cd Datasets; mkdir "'+userEntry+'";')
        os.system('cp copy-ShivamIoT.jpg Datasets/"'+userEntry+'"')
    else:
        aio.send_data(contents.key, items[userChoice-1])
    os.system('python receive-file.py')