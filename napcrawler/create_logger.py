from logging import WARNING, Formatter, Logger, StreamHandler, getLogger


def create_logger(name: str, level: int | str = WARNING) -> Logger:
    logger = getLogger(name)
    logger.setLevel(level)

    st_handler = StreamHandler()
    st_handler.setLevel(level)
    st_handler.setFormatter(Formatter("[%(asctime)s][%(levelname)s][%(filename)s:%(lineno)d] %(message)s"))
    logger.addHandler(st_handler)
    return logger


def change_logger_level(name: str, level: int | str):
    logger = getLogger(name)
    logger.setLevel(level)
    for handler in logger.handlers:
        handler.setLevel(level)
