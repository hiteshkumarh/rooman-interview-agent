import os
import logging
from typing import Optional

from dotenv import load_dotenv
from groq import (
    Groq,
    GroqError,
    APIConnectionError,
    APIStatusError,
    RateLimitError,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GroqClient:
    """
    Reusable Groq LLM client.

    Loads API credentials from a .env file and provides a simple interface
    to generate responses from the Groq Chat Completions API.
    """

    def __init__(self, env_path: Optional[str] = None):
        """
        Initialize the Groq client.

        Args:
            env_path (Optional[str]):
                Path to a custom .env file. If None, python-dotenv will
                automatically search for one.
        """

        # Load environment variables
        if env_path:
            load_dotenv(dotenv_path=env_path)
        else:
            load_dotenv()

        self.api_key = os.getenv("GROQ_API_KEY")
        self.model = os.getenv(
            "GROQ_MODEL",
            "llama-3.3-70b-versatile",
        )

        if not self.api_key:
            raise ValueError(
                "GROQ_API_KEY not found. "
                "Please add it to your .env file."
            )

        # Initialize Groq client
        self.client = Groq(api_key=self.api_key)

        logger.info(f"Groq client initialized with model: {self.model}")

    def generate_response(self, prompt: str) -> str:
        """
        Generate a response from the Groq LLM.

        Args:
            prompt (str):
                User prompt.

        Returns:
            str:
                Generated response.

        Raises:
            ValueError:
                If prompt is empty.

            ConnectionError:
                If network connection fails.

            RuntimeError:
                For API errors, authentication issues,
                rate limits, or unexpected failures.
        """

        if not isinstance(prompt, str) or not prompt.strip():
            raise ValueError("Prompt must be a non-empty string.")

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                temperature=0.4,
                max_tokens=1024,
            )

            if (
                response.choices
                and response.choices[0].message.content
            ):
                return response.choices[0].message.content.strip()

            logger.warning("Groq returned an empty response.")
            return ""

        except RateLimitError as e:
            logger.error(f"Rate limit exceeded: {e}")
            raise RuntimeError(
                "Groq API rate limit exceeded. Please try again later."
            ) from e

        except APIConnectionError as e:
            logger.error(f"Connection error: {e}")
            raise ConnectionError(
                "Unable to connect to the Groq API."
            ) from e

        except APIStatusError as e:
            logger.error(
                f"API Status Error {e.status_code}: {e.response}"
            )
            raise RuntimeError(
                f"Groq API returned status code {e.status_code}."
            ) from e

        except GroqError as e:
            logger.error(f"Groq SDK error: {e}")
            raise RuntimeError(
                f"Groq SDK error: {e}"
            ) from e

        except Exception as e:
            logger.exception("Unexpected error")
            raise RuntimeError(
                f"Unexpected error: {e}"
            ) from e