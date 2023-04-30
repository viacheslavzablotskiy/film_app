def get_path_upload_avatar(instance, file):
    """ Построение пути к файлу, format: (media)/avatar/user_id/photo.jpg
    """
    return f'my_image_and_video/avatar/user_{instance.id}/{file}'
