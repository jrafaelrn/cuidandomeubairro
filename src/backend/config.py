import os
import sys
import logging

log = logging.getLogger(__name__)


# Add path to SYS.PATH to import modules
def configure_paths(APP_PATH: str):
    sys.path.append(os.path.join(APP_PATH, "scripts"))
    sys.path.append(os.path.join(APP_PATH, "classes", "city"))
    sys.path.append(os.path.join(APP_PATH, "classes", "extractor"))
    log.debug(f'System paths: {sys.path}')