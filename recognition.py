import face_recognition
import helpers


def face_locations(img_path):
    image = face_recognition.load_image_file(img_path)
    face_landmarks_list = face_recognition.face_landmarks(image)

    size = 512, 512
    image_with_landmarks = helpers.highlight_face_marks(image, face_landmarks_list, size)

    return {
        "face_landmarks_list": face_landmarks_list,
        "image_with_landmarks": image_with_landmarks
    }
