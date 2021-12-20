"""
Helper functions for Tautulli_API
"""


def pms_image_proxy(img=None, rating_key=None, width=None, height=None,
                    opacity=None, background=None, blur=None, img_format=None,
                    fallback=None, refresh=None, clip=None):
    params = {}

    if img is not None:
        params['img'] = img
    if rating_key is not None:
        params['rating_key'] = rating_key
    if width is not None:
        params['width'] = width
    if height is not None:
        params['height'] = height
    if opacity is not None:
        params['opacity'] = opacity
    if background is not None:
        params['background'] = background
    if blur is not None:
        params['blur'] = blur
    if img_format is not None:
        params['img_format'] = img_format
    if fallback is not None:
        params['fallback'] = fallback
    if refresh is not None:
        params['refresh'] = 'true'
    if clip is not None:
        params['clip'] = 'true'

    return params


def info_page(rating_key=None, guid=None, history=None, live=None):
    params = {}

    if live and history:
        params['guid'] = guid
    else:
        params['rating_key'] = rating_key

    if history:
        params['source'] = 'history'

    return params


def library_page(section_id=None):
    params = {}

    if section_id is not None:
        params['section_id'] = section_id

    return params


def user_page(user_id=None, user=None):
    params = {}

    if user_id is not None:
        params['user_id'] = user_id
    if user is not None:
        params['user'] = user

    return params