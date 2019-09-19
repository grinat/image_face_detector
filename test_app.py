import os
import unittest
from app import app
from flask import json


class AppCase(unittest.TestCase):
    def test_face_landmarks(self):
        response = app.test_client().post(
            '/api/v1/face-landmarks',
            data={
                'image': (os.path.join(f"./fixtures/putin.jpg"), "img.jpg")
            },
            content_type='multipart/form-data',
        )

        self.assertEqual(response.status_code, 200)

        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(len(body['face_landmarks_list']) > 0, True)
        self.assertEqual(body['face_count'], 1)
        self.assertEqual('image' in body, True)

    def test_face_locations(self):
        response = app.test_client().post(
            '/api/v1/face-locations',
            data={
                'image': (os.path.join(f"./fixtures/putin.jpg"), "img.jpg")
            },
            content_type='multipart/form-data',
        )

        self.assertEqual(response.status_code, 200)

        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(len(body['face_locations']) > 0, True)
        self.assertEqual(body['face_count'], 1)
        self.assertEqual(len(body['images'][0]) > 0, True)

    def test_face_encodings(self):
        response = app.test_client().post(
            '/api/v1/face-encodings',
            data={
                'image': (os.path.join(f"./fixtures/putin.jpg"), "img.jpg")
            },
            content_type='multipart/form-data',
        )

        self.assertEqual(response.status_code, 200)

        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(len(body['face_encodings_list']) > 0, True)
        self.assertEqual(body['face_count'], 1)

    def test_compare_faces(self):
        response = app.test_client().post(
            '/api/v1/compare-faces',
            data=json.dumps({
                'haystack': [[-0.08118981122970581, 0.07731892168521881]],
                'needle': [-0.07118981122970582, 0.06731892168521882]
            }),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 200)

        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(body['faces'][0], True)


if __name__ == '__main__':
    unittest.main()
