import logging

from llm.client import GroqClient
from llm.prompts import FINAL_REPORT_PROMPT

logger = logging.getLogger(__name__)


class ReportGenerator:
    """
    Service for generating a comprehensive final interview report
    using the Groq LLM.
    """

    def __init__(self):
        """
        Initialize the ReportGenerator.
        """
        try:
            self.llm_client = GroqClient()
            logger.info("ReportGenerator initialized successfully.")
        except Exception as e:
            logger.exception("Failed to initialize GroqClient.")
            raise RuntimeError("Could not initialize Groq client.") from e

    def generate_report(
        self,
        role: str,
        skills: str,
        experience: str,
        questions: list[str],
        answers: list[str],
        evaluations: list[dict],
    ) -> str:
        """
        Generate a final interview report based on candidate's performance.

        Args:
            role: Target job role.
            skills: Required skills.
            experience: Candidate's experience level.
            questions: List of questions asked during the interview.
            answers: List of answers provided by the candidate.
            evaluations: List of evaluation dictionaries for each answer.

        Returns:
            The generated final report string.

        Raises:
            ValueError:
                If any input is empty or if lengths of lists mismatch.

            RuntimeError:
                If report generation fails.
        """

        self._validate_inputs(
            role,
            skills,
            experience,
            questions,
            answers,
            evaluations,
        )

        formatted_questions = self._format_questions(questions)
        formatted_answers = self._format_answers(answers)
        formatted_evaluations = self._format_evaluations(evaluations)

        prompt = FINAL_REPORT_PROMPT.format(
            role=role,
            skills=skills,
            experience=experience,
            questions=formatted_questions,
            answers=formatted_answers,
            evaluations=formatted_evaluations,
        )

        try:
            response = self.llm_client.generate_response(prompt)
            return response.strip()

        except Exception as e:
            logger.exception("Failed to generate report.")
            raise RuntimeError(
                f"Report generation failed: {e}"
            ) from e

    def _validate_inputs(
        self,
        role: str,
        skills: str,
        experience: str,
        questions: list[str],
        answers: list[str],
        evaluations: list[dict],
    ) -> None:
        """
        Validate all inputs for the report generator.
        """

        if not role.strip():
            raise ValueError("Role cannot be empty.")
        if not skills.strip():
            raise ValueError("Skills cannot be empty.")
        if not experience.strip():
            raise ValueError("Experience cannot be empty.")

        if not questions:
            raise ValueError("Questions list cannot be empty.")
        if not answers:
            raise ValueError("Answers list cannot be empty.")
        if not evaluations:
            raise ValueError("Evaluations list cannot be empty.")

        if not (len(questions) == len(answers) == len(evaluations)):
            raise ValueError(
                "Questions, answers, and evaluations must have the same length."
            )

    def _format_questions(
        self,
        questions: list[str],
    ) -> str:
        """
        Convert a list of questions into a numbered string.
        """
        formatted = []
        for i, q in enumerate(questions, 1):
            formatted.append(f"{i}. {q.strip()}")
        return "\n".join(formatted)

    def _format_answers(
        self,
        answers: list[str],
    ) -> str:
        """
        Convert a list of answers into a numbered string with sections.
        """
        formatted = []
        for i, a in enumerate(answers, 1):
            formatted.append(f"Answer {i}:\n{a.strip()}")
        return "\n\n".join(formatted)

    def _format_evaluations(
        self,
        evaluations: list[dict],
    ) -> str:
        """
        Convert a list of evaluation dictionaries into readable text.
        """
        formatted = []
        for i, eval_dict in enumerate(evaluations, 1):
            parts = [f"Evaluation {i}:"]

            score = eval_dict.get("score")
            score_str = str(score) if score is not None else "N/A"
            parts.append(f"Score: {score_str}")

            parts.append("Strengths:")
            parts.append(self._join_bullets(eval_dict.get("strengths", [])))

            parts.append("Weaknesses:")
            parts.append(self._join_bullets(eval_dict.get("weaknesses", [])))

            parts.append("Missing Concepts:")
            parts.append(self._join_bullets(eval_dict.get("missing_concepts", [])))

            parts.append("Ideal Answer:")
            parts.append(eval_dict.get("ideal_answer", "Not Available"))

            parts.append("Suggestions:")
            parts.append(self._join_bullets(eval_dict.get("suggestions", [])))

            formatted.append("\n".join(parts))

        return "\n\n".join(formatted)

    def _join_bullets(
        self,
        items: list[str],
    ) -> str:
        """
        Join a list of strings into bullet points safely.
        """
        if not items:
            return "None"
        return "\n".join(
            f"- {item}"
            for item in items
            if item.strip()
        )
