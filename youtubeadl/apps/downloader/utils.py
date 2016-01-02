import uuid

import youtube_dl

from youtubeadl.apps.core.utils import slugify


def create_filename(value):
    """
    Generate a valid filename.

    Non-ASCII characters will be deleted from the value and replace spaces with
    underscores. Slashes and percent signs are also stripped.
    """
    filename = slugify(value, u'_')

    # Generate a random filename if the title only contains non-ASCII
    # characters (i.e. slugifying it deletes everything).
    if not filename:
        filename = uuid.uuid4()

    return '{}.mp3'.format(filename)


def get_video_info(url):
    """
    Retrieve the YouTube videos' information without downloading it.

    Source: http://stackoverflow.com/questions/18054500/how-to-use-youtube-dl-\
            from-a-python-programm/18947879#18947879
    """
    ydl = youtube_dl.YoutubeDL()
    ydl.add_default_info_extractors()

    try:
        return ydl.extract_info(url, download=False)
    except youtube_dl.DownloadError:
        return None