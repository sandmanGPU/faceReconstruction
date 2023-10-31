import os
import joblib
from box.exceptions import BoxValueError
import yaml
import json
from src.facereconstrcut import logger
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path
from typing import AnyStr
import base64

@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """reads yaml file and returns

    Args:
        path_to_yaml (str): Path like input

    Raises:
        ValueError: if yaml file is empty, i.e. contains no content
        e: empty file

    Returns:
        ConfigBox: ConfigBox type
    """

    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"yaml file: {path_to_yaml} loaded successfully")
            return ConfigBox(content)
    except BoxValueError:
        
        raise ValueError(f"yaml file is empty @ {path_to_yaml}")
    except Exception as e:
        raise e
    
@ensure_annotations
def create_directories(pathdirs: list, verbose=True):
    for path in pathdirs:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"created dir @: {path}")


@ensure_annotations
def save_json(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)
    logger.info(f'json file saved at: {path}')

@ensure_annotations
def load_json(path: Path)->ConfigBox:
    with open(path) as f:
        content=json.load(f)
    logger.info(f'json file loaded successfully from: {path}')
    return ConfigBox(content)

@ensure_annotations
def get_size(path: Path) -> str:
    """get size in KB

    Args:
        path (Path): path of the file

    Returns:
        str: size in KB
    """
    size_in_kB = round(os.path.getsize(path) / 1024)
    return f"~{size_in_kB}kB"


def decodeImage(imgstring, filename):
    imgdata = base64.b64decode(imgstring)
    with open(filename, 'wb') as f:
        f.write(imgdata)
        f.close()


def encodeImageIntoBase64(croppedImagePath):
    with(croppedImagePath, 'rb') as f:
        return base64.b64decode(f.read())