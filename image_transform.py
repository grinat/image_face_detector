from PIL import ImageFont, Image, ImageDraw
from io import BytesIO

BLUE = (55, 0, 255)
GREEN = (0, 255, 0)
GREEN_LIGHT = (208, 255, 0)


# higlight face marks on image
def highlight_face_marks(image, face_landmarks_list, size):
    pil_image = Image.fromarray(image)

    for face_landmarks in face_landmarks_list:
        d = ImageDraw.Draw(pil_image, 'RGBA')

        # Calc font size
        font_size_to_nose_ratio = 0.6
        nose_start = face_landmarks['nose_bridge'][0]
        nose_end = face_landmarks['nose_bridge'][len(face_landmarks['nose_bridge']) - 1]
        font_size = nose_start[1] - nose_end[1]
        if font_size < 0:
            font_size = font_size * -1
        font_size = round(font_size * font_size_to_nose_ratio)
        font = ImageFont.truetype('assets/Roboto-Bold.ttf', font_size)

        d.line(face_landmarks['top_lip'], fill=GREEN_LIGHT, width=6)
        d.line(face_landmarks['bottom_lip'], fill=GREEN_LIGHT, width=6)

        d.polygon(face_landmarks['right_eye'], fill=BLUE)
        d.polygon(face_landmarks['left_eye'], fill=BLUE)

        d.line(face_landmarks['nose_bridge'], fill=GREEN_LIGHT, width=6)

        d.line(face_landmarks['chin'], fill=GREEN, width=6)

        # Draw text on center of chin
        txt_coord_index = round(len(face_landmarks['chin']) / 2)
        d.text(face_landmarks['chin'][txt_coord_index], "Contour", font=font, fill=GREEN)

    buffered = BytesIO()
    pil_image.thumbnail(size)
    pil_image.save(buffered, format="JPEG")

    return buffered


# put every face in separatly image
def crop_faces(image, face_locations_list, size):
    faces = []

    for face_location in face_locations_list:
        bottom, right, top, left = face_location

        face_image = image[bottom:top, left:right]
        pil_image = Image.fromarray(face_image)

        buffered = BytesIO()
        pil_image.thumbnail(size)
        pil_image.save(buffered, format="JPEG")

        faces.append(buffered)

    return faces
