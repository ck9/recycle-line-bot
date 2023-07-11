import os
import requests
from google.cloud import vision
from google.oauth2 import service_account

this_dir = os.path.dirname(os.path.abspath(__file__))

class VisionAI:

    credentials = service_account.Credentials.from_service_account_file(os.path.join(this_dir, 'vision_ai-key.json'))
    client = vision.ImageAnnotatorClient(credentials=credentials)

    # 画像からオブジェクトを検出(引数:画像URL, 戻り値:オブジェクト名リスト)
    def object_localization(self, image):
        response = self.client.object_localization(image=image)
        localized_object_annotations = response.localized_object_annotations
        # print('Number of objects found: {}'.format(len(localized_object_annotations)))
        object_list = []
        for obj in localized_object_annotations:
            object_list.append(obj.name)
            print('{} : {}%'.format(obj.name, obj.score))
            # print('Normalized bounding polygon vertices: ')
            # for vertex in obj.bounding_poly.normalized_vertices:
            #     print(' - ({}, {})'.format(vertex.x, vertex.y))
        if response.error.message:
            raise Exception(
                '{}\nFor more info on error messages, check: '
                'https://cloud.google.com/apis/design/errors'.format(
                    response.error.message))
        # 重複オブジェクトを削除
        object_list = list(set(object_list))
        return object_list

    def recognize_path(self, image_path):
        with open(image_path, 'rb') as image_file:
            content = image_file.read()
        image = vision.Image(content=content)
        return self.object_localization(image)
    
    def recognize_url(self, image_url):
        image = vision.Image()
        image.source.image_uri = image_url
        return self.object_localization(image)
        

class Rekognition:
    import boto3, json
    
    with open(os.path.join(this_dir, 'rekognition-key.json')) as f:
        credentials = json.load(f)
    region = credentials['region']
    awsaccesskeyid = credentials['awsaccesskeyid']
    awssecretkey = credentials['awssecretkey']

    client = boto3.client('rekognition', region_name=region, aws_access_key_id=awsaccesskeyid, aws_secret_access_key=awssecretkey)

    def recognize_path(self, image_path):
        with open(image_path, 'rb') as image_file:
            content = image_file.read()
        response = self.client.detect_labels(Image={'Bytes': content}, MaxLabels=10)
        labels = []
        for label in response['Labels']:
            print(label['Name'] + ' : ' + str(label['Confidence']) + '%')
            if label['Confidence'] > 95 and label['Name'] not in labels:
                labels.append(label['Name'])
        return labels
    
if __name__ == '__main__':
    image_url = input("img_url:")

    print("VisionAI")
    vision_ai = VisionAI()
    print(vision_ai.recognize_url(image_url))

    print("Rekognition")
    rekognition = Rekognition()
    img = requests.get(image_url)
    tmp_path = os.path.join(this_dir, 'tmp.jpg')
    with open(tmp_path, 'wb') as f:
        f.write(img.content)
    print(rekognition.recognize_path(tmp_path))
    os.remove(tmp_path)