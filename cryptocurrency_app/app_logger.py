"""Module to create app loger."""

from os import path as os_path, getenv as os_getenv
from pathlib import Path
from logging import Formatter, Logger, StreamHandler, getLogger
from logging.handlers import RotatingFileHandler

class CustomLogger:
    """Base class CustomLogger. Class create logger for app."""

    @classmethod
    def get_logger(cls, logger_name: str) -> Logger:
        """Create app logger."""

        logger = getLogger(logger_name)
        logger.handlers.clear()
        for i_handler in (
                cls._get_stream_handler(), cls._get_rotating_file_handler()
        ):
            logger.addHandler(i_handler)
        logger.setLevel(os_getenv("LOGGER_LEVEL"))
        return logger

    @classmethod
    def _get_logs_dir_path(cls) -> str:
        """Get logs saving path."""

        log_path = os_path.join(
            os_path.dirname(os_path.realpath(__file__)),
            os_getenv("LOGGER_FILES_DIR_NAME"),
        )

        return os_path.abspath(log_path)

    @classmethod
    def _get_stream_handler(cls) -> StreamHandler:
        """Create stream handler for logger."""

        stream_handler = StreamHandler()
        stream_handler.setLevel(os_getenv("LOGGER_STREAM_HANDLER_LEVEL"))
        formatter = Formatter(
            "*** %(asctime)s | %(name)s | %(funcName)s | "
            "%(levelname)s | %(message)s",
        )
        stream_handler.setFormatter(formatter)
        return stream_handler

    @classmethod
    def _create_directory(cls, abs_path: str) -> None:
        """Create path if it is not existed."""

        Path(abs_path).mkdir(parents=True, exist_ok=True)

    @classmethod
    def _get_rotating_file_handler(cls) -> RotatingFileHandler:
        """Create rotating file handler for logger."""

        logs_path = cls._get_logs_dir_path()
        cls._create_directory(logs_path)
        logs_file_path = os_path.join(
            logs_path, os_getenv("LOGGER_FILES_NAME")
        )
        rotating_file_handler = RotatingFileHandler(
            filename=logs_file_path,
            mode="a",
            maxBytes=int(os_getenv("LOGGER_FILE_SIZE")),
            backupCount=int(os_getenv("LOGGER_BACKUP_COUNT")),
            encoding=os_getenv("ENCODING"),
        )
        rotating_file_handler.setLevel(os_getenv("LOGGER_FILE_HANDLER_LEVEL"))
        formatter = Formatter(
            "%(asctime)s|%(name)s|%(funcName)s|%(levelname)s|%(message)s",
        )
        rotating_file_handler.setFormatter(formatter)
        return rotating_file_handler


app_logger = CustomLogger.get_logger(os_getenv("LOGGER_NAME"))
