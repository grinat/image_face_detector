import face_recognition
import image_transform
import numpy as np


def face_landmarks(img_path, out_sz):
    image = face_recognition.load_image_file(img_path)
    face_landmarks_list = face_recognition.face_landmarks(image)

    size = (out_sz, out_sz)
    image_with_landmarks = image_transform.highlight_face_marks(image, face_landmarks_list, size)

    return {
        "face_landmarks_list": face_landmarks_list,
        "image_with_landmarks": image_with_landmarks
    }


def face_locations(img_path, out_sz):
    image = face_recognition.load_image_file(img_path)
    face_locations_list = face_recognition.face_locations(image)

    size = (out_sz, out_sz)
    images = image_transform.crop_faces(image, face_locations_list, size)

    return {
        "face_locations_list": face_locations_list,
        "images": images
    }


def face_encodings(img_path):
    image = face_recognition.load_image_file(img_path)
    face_encodings_np_list = face_recognition.face_encodings(image)

    return {
        "face_encodings_list": _np_array_to_list(face_encodings_np_list)
    }


def compare(haystack, needle):
    # we convert python list to numpy
    needle_np = np.array(needle)
    haystack_np_list = []
    for face in haystack:
        haystack_np_list.append(np.array(face))

    # compares numpy arrays
    distances_np = face_recognition.face_distance(haystack_np_list, needle_np)

    distances = []
    for res_np in distances_np:
        distances.append(res_np.tolist())

    return {
        "face_distances": distances
    }


# todo: remove face_recognition lib, write own implementation
def face_metrics(img_path):
    image = face_recognition.load_image_file(img_path)

    # get landmarks
    face_landmarks_list = face_recognition.face_landmarks(image)

    # get encodings
    face_encodings_list = _np_array_to_list(face_recognition.face_encodings(image))

    # get face top, right, bottom, left
    face_locations_list = face_recognition.face_locations(image)

    return {
        'face_landmarks_list': face_landmarks_list,
        'face_encodings_list': face_encodings_list,
        'face_locations_list': face_locations_list
    }


def _np_array_to_list(np_list):
    return [item.tolist() for item in np_list]
