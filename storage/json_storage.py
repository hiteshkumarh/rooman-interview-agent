import json
import logging
import os
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)


class JSONStorage:
    """
    Storage service for managing interview transcripts in JSON format.
    """

    def __init__(self, storage_dir: str = "storage/transcripts"):
        """
        Initialize the JSONStorage service.

        Args:
            storage_dir: The directory to store JSON files.
                         Defaults to "storage/transcripts".
        """
        self.storage_path = Path(storage_dir)

        try:
            self.storage_path.mkdir(parents=True, exist_ok=True)
            logger.info("JSONStorage initialized at: %s", self.storage_path.resolve())
        except Exception as e:
            logger.exception("Failed to create storage directory.")
            raise RuntimeError(f"Could not create storage directory: {e}") from e

    def save_interview(self, data: dict) -> str:
        """
        Save the interview data as a formatted JSON file.

        Args:
            data: The interview data dictionary.

        Returns:
            str: The saved file path.

        Raises:
            ValueError: If the input is not a dictionary.
            RuntimeError: If saving the file fails.
        """
        if not isinstance(data, dict):
            logger.error("Provided data is not a dictionary.")
            raise ValueError("Data must be a dictionary.")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"interview_{timestamp}.json"
        file_path = self.storage_path / filename

        try:
            with file_path.open("w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            logger.info("Successfully saved interview to: %s", file_path)
            return str(file_path)
        except Exception as e:
            logger.exception("Failed to save interview data.")
            raise RuntimeError(f"Failed to save interview data: {e}") from e

    def load_interview(self, file_path: str) -> dict:
        """
        Load interview data from a JSON file.

        Args:
            file_path: Path to the JSON file.

        Returns:
            dict: The interview data.

        Raises:
            ValueError: If the file path is empty or invalid.
            FileNotFoundError: If the file does not exist.
            RuntimeError: If JSON decoding or reading fails.
        """
        if not file_path or not str(file_path).strip():
            logger.error("Empty file path provided.")
            raise ValueError("File path cannot be empty.")

        path = Path(file_path)

        if not path.exists():
            logger.error("File not found: %s", file_path)
            raise FileNotFoundError(f"File does not exist: {file_path}")

        if not path.is_file():
            logger.error("Path is not a file: %s", file_path)
            raise ValueError(f"Path is not a valid file: {file_path}")

        try:
            with path.open("r", encoding="utf-8") as f:
                data = json.load(f)
            logger.info("Successfully loaded interview from: %s", file_path)
            return data
        except json.JSONDecodeError as e:
            logger.exception("JSON decoding failed for file: %s", file_path)
            raise RuntimeError(f"Invalid JSON format: {e}") from e
        except Exception as e:
            logger.exception("Failed to load interview data.")
            raise RuntimeError(f"Failed to load interview data: {e}") from e

    def list_interviews(self) -> list[str]:
        """
        Return all saved JSON filenames, sorted by newest first.

        Returns:
            list[str]: List of filenames.
        """
        try:
            files = list(self.storage_path.glob("*.json"))
            # Sort by modification time (newest first)
            files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            return [f.name for f in files]
        except Exception as e:
            logger.exception("Failed to list interviews.")
            raise RuntimeError(f"Failed to list interviews: {e}") from e

    def delete_interview(self, file_path: str) -> bool:
        """
        Delete a specified JSON file.

        Args:
            file_path: Path to the JSON file.

        Returns:
            bool: True if deleted successfully, False if file did not exist.

        Raises:
            ValueError: If the file path is empty.
            RuntimeError: If deletion fails due to an OS error.
        """
        if not file_path or not str(file_path).strip():
            logger.error("Empty file path provided for deletion.")
            raise ValueError("File path cannot be empty.")

        path = Path(file_path)

        if not path.exists() or not path.is_file():
            logger.warning("File does not exist for deletion: %s", file_path)
            return False

        try:
            path.unlink()
            logger.info("Successfully deleted interview file: %s", file_path)
            return True
        except Exception as e:
            logger.exception("Failed to delete interview file.")
            raise RuntimeError(f"Failed to delete file: {e}") from e
