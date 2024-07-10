import os
from pathlib import Path
from typing import Any
from app.service import FaceVerificationService
from app.main import main
import pytest


@pytest.fixture
def test_data_dir() -> str:
    test_data_dir = 'src/tests/test_data/'
    test_data_dir_path = Path(test_data_dir)
    if not test_data_dir_path.is_dir():
        os.mkdir(test_data_dir_path)
    return test_data_dir


@pytest.fixture
def representation(test_data_dir: str) -> list[dict[str, Any]]:
    img = 'me.jpg'
    img_full_path = test_data_dir + img
    service = FaceVerificationService()
    return service.represent(img_full_path)


def test_representation_is_not_empty(representation: list[dict[str, Any]]) -> None:
    assert representation is not None
    assert len(representation) > 0


def test_main_without_error():
    main()
