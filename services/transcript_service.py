import logging

from storage.json_storage import JSONStorage

logger = logging.getLogger(__name__)


class TranscriptService:
    """
    Service for managing interview transcripts.
    This acts as an abstraction layer over the underlying storage mechanism.
    """

    def __init__(self):
        """
        Initialize the TranscriptService and its storage mechanism.
        """
        try:
            self.storage = JSONStorage()
            logger.info("TranscriptService initialized successfully.")
        except Exception as e:
            logger.exception("Failed to initialize TranscriptService.")
            raise RuntimeError(f"Could not initialize TranscriptService: {e}") from e

    def save_interview(self, data: dict) -> str:
        """
        Save the interview data to storage.

        Args:
            data: The interview data dictionary to save.

        Returns:
            The file path where the interview was saved.

        Raises:
            ValueError: If the input data is invalid.
            RuntimeError: If saving fails.
        """
        if not isinstance(data, dict):
            logger.error("Invalid data type for saving interview. Expected dict.")
            raise ValueError("Data must be a dictionary.")

        try:
            return self.storage.save_interview(data)
        except Exception as e:
            logger.exception("Error in TranscriptService while saving interview.")
            raise RuntimeError(f"Failed to save interview: {e}") from e

    def load_interview(self, file_path: str) -> dict:
        """
        Load interview data from a given file path.

        Args:
            file_path: The path to the interview transcript.

        Returns:
            The loaded interview data as a dictionary.

        Raises:
            ValueError: If the file path is empty.
            FileNotFoundError: If the file does not exist.
            RuntimeError: If loading fails.
        """
        if not file_path or not str(file_path).strip():
            logger.error("Empty file path provided for loading.")
            raise ValueError("File path cannot be empty.")

        try:
            return self.storage.load_interview(file_path)
        except FileNotFoundError:
            raise
        except ValueError:
            raise
        except Exception as e:
            logger.exception("Error in TranscriptService while loading interview.")
            raise RuntimeError(f"Failed to load interview: {e}") from e

    def list_interviews(self) -> list[str]:
        """
        List all saved interview transcripts.

        Returns:
            A list of file names representing saved interviews.

        Raises:
            RuntimeError: If listing fails.
        """
        try:
            return self.storage.list_interviews()
        except Exception as e:
            logger.exception("Error in TranscriptService while listing interviews.")
            raise RuntimeError(f"Failed to list interviews: {e}") from e

    def delete_interview(self, file_path: str) -> bool:
        """
        Delete an interview transcript.

        Args:
            file_path: The path of the interview to delete.

        Returns:
            True if deleted successfully, False if the file was not found.

        Raises:
            ValueError: If the file path is invalid.
            RuntimeError: If deletion fails.
        """
        if not file_path or not str(file_path).strip():
            logger.error("Empty file path provided for deletion.")
            raise ValueError("File path cannot be empty.")

        try:
            return self.storage.delete_interview(file_path)
        except Exception as e:
            logger.exception("Error in TranscriptService while deleting interview.")
            raise RuntimeError(f"Failed to delete interview: {e}") from e
