def get_path_upload_cover_image(instance, file):
    """ Построение пути к файлу, format: (media)/album/user_id/photo.jpg
    """
    return f'image/user_{instance.user.id}/{file}'
