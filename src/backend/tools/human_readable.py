import time

def convert_seconds_to_human_readable(seconds):
    """
    Convert seconds to human readable format.
    :param seconds: seconds to convert
    :return: human readable format hh:mm:ss
    """
    return time.strftime('%H:%M:%S', time.gmtime(seconds))