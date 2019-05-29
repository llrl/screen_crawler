__all__ = ['get_content']

from dragnet import extract_content

def get_content(raw_site_data):
    return extract_content(raw_site_data)