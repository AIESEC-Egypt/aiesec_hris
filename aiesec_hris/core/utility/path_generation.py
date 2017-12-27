"""
Helpers for generating file paths.
Author: Ahmed H. Ismail
"""


def profile_photo_path(instance, filename):
    """
    Path for  a profile's photo
    """
    return 'uploads/profile_portraits_{0}/portrait_{1}'.format(
        instance.pk, filename)


def national_id_path(instance, filename):
    """
    Path for a national id photo.
    """
    return 'uploads/profile_national_ids_{0}/national_id_{1}'.format(
        instance.pk, filename)
