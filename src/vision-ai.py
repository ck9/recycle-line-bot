import os
from google.cloud import vision
from google.oauth2 import service_account

this_dir = os.path.dirname(os.path.abspath(__file__))

credentials = service_account.Credentials.from_service_account_file(os.path.join(this_dir, 'vision-ai-key.json'))
client = vision.ImageAnnotatorClient(credentials=credentials)

# def label_detection(image):
#     response = client.label_detection(image=image)
#     labels = response.label_annotations
#     print('Labels:')
#     for label in labels:
#         print(label.description)
#     if response.error.message:
#         raise Exception(
#             '{}\nFor more info on error messages, check: '
#             'https://cloud.google.com/apis/design/errors'.format(
#                 response.error.message))

def object_localization(image):
    response = client.object_localization(image=image)
    localized_object_annotations = response.localized_object_annotations
    print('Number of objects found: {}'.format(len(localized_object_annotations)))
    object_list = []
    for obj in localized_object_annotations:
        object_list.append(obj.name)
        print('\n{} (confidence: {})'.format(obj.name, obj.score))
        print('Normalized bounding polygon vertices: ')
        for vertex in obj.bounding_poly.normalized_vertices:
            print(' - ({}, {})'.format(vertex.x, vertex.y))
    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
    return object_list

def main(img_url=None):
    if img_url is None:
        img_url = input("img_url:")
    image = vision.Image()
    image.source.image_uri = img_url
    return object_localization(image)
    
if __name__ == '__main__':
    main()