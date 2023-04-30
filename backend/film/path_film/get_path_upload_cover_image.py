def get_path_upload_cover_image(instance, file):
    """ Построение пути к файлу, format: (media)/album/user_id/photo.jpg
    """
    return f'my_image_and_video/image/user_{instance.user.id}/{file}'
