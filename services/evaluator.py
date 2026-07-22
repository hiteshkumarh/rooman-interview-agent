import logging
import re
from typing import Any, Dict, List

from llm.client import GroqClient
from llm.prompts import ANSWER_EVALUATION_PROMPT

logger = logging.getLogger(__name__)


class AnswerEvaluator:
    """
    Service for evaluating interview answers using the Groq LLM.
    """

    def __init__(self):
        """
        Initialize the AnswerEvaluator.
        """
        try:
            self.llm_client = GroqClient()
            logger.info("AnswerEvaluator initialized successfully.")
        except Exception as e:
            logger.exception("Failed to initialize GroqClient.")
            raise RuntimeError("Could not initialize Groq client.") from e

    def evaluate_answer(self, question: str, answer: str) -> Dict[str, Any]:
        """
        Evaluate a candidate's answer.

        Args:
            question: Interview question.
            answer: Candidate answer.

        Returns:
            Dictionary containing evaluation details.

        Raises:
            ValueError:
                If question or answer is empty.

            RuntimeError:
                If evaluation fails.
        """

        if not question.strip():
            raise ValueError("Question cannot be empty.")

        if not answer.strip():
            raise ValueError("Answer cannot be empty.")

        prompt = ANSWER_EVALUATION_PROMPT.format(
            question=question,
            answer=answer,
        )

        try:
            response = self.llm_client.generate_response(prompt)
            return self._parse_evaluation(response)

        except Exception as e:
            logger.exception("Failed to evaluate answer.")
            raise RuntimeError(
                f"Evaluation failed: {e}"
            ) from e

    def _parse_evaluation(self, response_text: str) -> Dict[str, Any]:
        """
        Parse the LLM response into a structured dictionary.
        """

        result = {
            "score": None,
            "strengths": [],
            "weaknesses": [],
            "missing_concepts": [],
            "ideal_answer": "",
            "suggestions": [],
            "raw_response": response_text,
        }

        try:
            # ---------------- Score ----------------

            score_match = re.search(
                r"(?i)score\s*[:\-]?\s*(\d+)",
                response_text,
            )

            if score_match:
                score = int(score_match.group(1))
                result["score"] = max(0, min(score, 10))

            # ------------- Sections ----------------

            result["strengths"] = self._parse_bullets(
                self._extract_section(
                    response_text,
                    "Strengths",
                )
            )

            result["weaknesses"] = self._parse_bullets(
                self._extract_section(
                    response_text,
                    "Weaknesses",
                )
            )

            result["missing_concepts"] = self._parse_bullets(
                self._extract_section(
                    response_text,
                    "Missing Concepts",
                )
            )

            result["suggestions"] = self._parse_bullets(
                self._extract_section(
                    response_text,
                    "Suggestions",
                )
            )

            result["ideal_answer"] = self._extract_section(
                response_text,
                "Ideal Answer",
            )

        except Exception as e:
            logger.warning(
                "Unable to fully parse LLM response: %s",
                e,
            )

        return result

    def _extract_section(
        self,
        text: str,
        section_name: str,
    ) -> str:
        """
        Extract a named section from the LLM response.
        """

        sections = [
            "Score",
            "Strengths",
            "Weaknesses",
            "Missing Concepts",
            "Ideal Answer",
            "Suggestions",
        ]

        other_sections = [
            s for s in sections
            if s != section_name
        ]

        pattern = (
            rf"{section_name}\s*:?\s*"
            rf"(.*?)"
            rf"(?=\n(?:{'|'.join(other_sections)})\s*:|\Z)"
        )

        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE | re.DOTALL,
        )

        if match:
            return match.group(1).strip()

        return ""

    def _parse_bullets(
        self,
        text: str,
    ) -> List[str]:
        """
        Convert a bullet-point section into a Python list.
        """

        if not text:
            return []

        bullets = []

        for line in text.splitlines():

            line = line.strip()

            if not line:
                continue

            line = re.sub(
                r"^[-*•]\s*",
                "",
                line,
            )

            line = re.sub(
                r"^\d+[\.\)]\s*",
                "",
                line,
            )

            if line:
                bullets.append(line)

        return bullets