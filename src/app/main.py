import logging

from app.service import FaceVerificationService


def main() -> None:
    """
    Точка входа в программу.

    Служит для задания точки входа в программу.
    """
    logging.basicConfig(level=logging.DEBUG)
    fvs = FaceVerificationService()
    img = 'src/tests/test_data/me.jpg'
    logging.info(fvs.represent(img_path=img))


if __name__ == '__main__':
    main()
