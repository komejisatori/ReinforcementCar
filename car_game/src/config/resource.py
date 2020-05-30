import os

# Global Path definition
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
RESOURCE_DIR_NAME = 'resource'
RESOURCE_IMAGE_DIR_NAME = 'imgs'
RESOURCE_IMAGE_PATH = os.path.abspath(os.path.join(ROOT_DIR, RESOURCE_DIR_NAME, RESOURCE_IMAGE_DIR_NAME))


# Resource File
IMAGE_COVER_FILE_PATH = os.path.join(RESOURCE_IMAGE_PATH, 'cover.jpg')
IMAGE_CAR_FILE_PATH = os.path.join(RESOURCE_IMAGE_PATH, 'car.png')
IMAGE_ICON_FILE_PATH = os.path.join(RESOURCE_IMAGE_PATH, 'icon.png')
IMAGE_WIN_FILE_PATH = os.path.join(RESOURCE_IMAGE_PATH, 'win.png')
