import uuid, os


def save_file_and_return_path(request):
    file_path = "uploads/" + str(uuid.uuid4()) + ".jpg"

    f = request.files['image']
    f.save(file_path)

    return file_path


def remove_file(file_path):
    os.remove(file_path)
