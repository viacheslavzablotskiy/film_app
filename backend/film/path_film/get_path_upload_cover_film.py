def get_path_upload_film(instance, file):
    """ Построение пути к файлу, format: (media)/avatar/user_id/photo.jpg
    """
    return f'my_image_and_video/video/user_{instance.user.id}/{file}'
