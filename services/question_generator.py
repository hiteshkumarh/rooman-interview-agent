import logging
import re

from llm.client import GroqClient
from llm.prompts import QUESTION_GENERATION_PROMPT

logger = logging.getLogger(__name__)

class QuestionGenerator:
    """
    Service for generating interview questions using the Groq LLM.
    """

    def __init__(self):
        """
        Initialize the QuestionGenerator with a GroqClient instance.
        """
        try:
            self.client = GroqClient()
            logger.info("QuestionGenerator initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize GroqClient in QuestionGenerator: {e}")
            raise

    def generate_questions(self, role: str, skills: str, experience: str) -> list[str]:
        """
        Generate a list of exactly 5 interview questions based on candidate details.

        Args:
            role (str): The role the candidate is applying for.
            skills (str): The candidate's skills.
            experience (str): The candidate's experience level.

        Returns:
            list[str]: A list of exactly 5 cleaned interview questions.

        Raises:
            ValueError: If fewer than 5 questions are generated or input is invalid.
            RuntimeError: If there is an issue with generating questions via the LLM.
        """
        if not all([
            role.strip(),
            skills.strip(),
            experience.strip(),
        ]):
            raise ValueError(
                "Role, skills, and experience must be non-empty strings."
    )
        try:
            # Format the prompt
            prompt = QUESTION_GENERATION_PROMPT.format(
                role=role,
                skills=skills,
                experience=experience
            )
            
            # Get response from the LLM
            logger.info(f"Generating questions for role: {role}")
            response_text = self.client.generate_response(prompt)
            
            if not response_text:
                raise RuntimeError("Received an empty response from the LLM.")

            # Parse the response
            questions = self._parse_questions(response_text)
            
            if len(questions) < 5:
                logger.error(f"Expected at least 5 questions, but generated {len(questions)}: {questions}")
                raise ValueError("The LLM generated fewer than 5 questions.")
                
            # Return exactly 5 questions
            return questions[:5]

        except ValueError:
            raise
        except Exception as e:
            logger.exception("Error generating questions.")
            raise RuntimeError(f"Failed to generate questions: {e}") from e

    def _parse_questions(self, text: str) -> list[str]:
        """
        Parse raw text into a cleaned list of questions.

        Removes numbering (e.g., '1.', '2)', '-', etc.) and ignores empty lines.

        Args:
            text (str): The raw text output from the LLM.

        Returns:
            list[str]: A list of cleaned question strings.
        """
        questions = []
        
        for line in text.splitlines():
            line = line.strip()
            # Ignore empty lines
            if not line:
                continue
                
            # Remove numbering like "1.", "1)", "-", "*", etc. at the start of the line
            clean_line = re.sub(
                r"^\s*(?:\d+[\.\)]|[-*•])\s*",
                "",
                line,
            ).strip()            
            # Avoid adding lines that became empty after cleaning, or very short noise lines
            if clean_line:
                questions.append(clean_line)
                    
        return questions
