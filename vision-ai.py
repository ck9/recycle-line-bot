from google.cloud import vision
from google.oauth2 import service_account

credentials = service_account.Credentials.from_service_account_file('vision-ai-key.json')
client = vision.ImageAnnotatorClient(credentials=credentials)

def label_detection(image):
    response = client.label_detection(image=image)
    labels = response.label_annotations
    print('Labels:')
    for label in labels:
        print(label.description)
    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

def object_localization(image):
    response = client.object_localization(image=image)
    localized_object_annotations = response.localized_object_annotations
    print('Number of objects found: {}'.format(len(localized_object_annotations)))
    for obj in localized_object_annotations:
        print('\n{} (confidence: {})'.format(obj.name, obj.score))
        print('Normalized bounding polygon vertices: ')
        for vertex in obj.bounding_poly.normalized_vertices:
            print(' - ({}, {})'.format(vertex.x, vertex.y))
    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

def main():
    img_url = input("img_url:")
    image = vision.Image()
    image.source.image_uri = img_url
    object_localization(image)
    # label_detection(image)

if __name__ == '__main__':
    main()