import logging
import os
import shutil
from enum import StrEnum
from pathlib import Path

import pytest

from app.service import FaceVerificationService, ModelName
