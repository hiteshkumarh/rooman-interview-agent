import logging

from services.question_generator import QuestionGenerator
from services.evaluator import AnswerEvaluator
from services.report_generator import ReportGenerator

logger = logging.getLogger(__name__)


class InterviewService:
    """
    Service that coordinates the interview workflow, including generating
    questions, evaluating answers, and generating the final report.
    """

    def __init__(self):
        """
        Initialize the InterviewService and its dependent services.
        """
        try:
            self.question_generator = QuestionGenerator()
            self.answer_evaluator = AnswerEvaluator()
            self.report_generator = ReportGenerator()
            logger.info("InterviewService initialized successfully.")
        except Exception as e:
            logger.exception("Failed to initialize InterviewService.")
            raise RuntimeError(
                f"Failed to initialize InterviewService: {e}"
            ) from e

    def start_interview(
        self,
        role: str,
        skills: str,
        experience: str,
    ) -> list[str]:
        """
        Generate interview questions.

        Args:
            role: Candidate's target role.
            skills: Candidate's skills.
            experience: Candidate's experience.

        Returns:
            List of exactly 5 interview questions.
        """

        if not role.strip():
            raise ValueError("Role cannot be empty.")

        if not skills.strip():
            raise ValueError("Skills cannot be empty.")

        if not experience.strip():
            raise ValueError("Experience cannot be empty.")

        try:
            questions = self.question_generator.generate_questions(
                role=role,
                skills=skills,
                experience=experience,
            )

            if len(questions) != 5:
                raise ValueError(
                    "Exactly 5 interview questions must be generated."
                )

            return questions

        except Exception as e:
            logger.exception("Failed to start interview.")
            raise RuntimeError(
                f"Could not start interview: {e}"
            ) from e

    def evaluate_interview(
        self,
        role: str,
        skills: str,
        experience: str,
        questions: list[str],
        answers: list[str],
    ) -> dict:
        """
        Evaluate candidate answers and generate the final report.

        Returns:
            Dictionary containing:
                questions
                answers
                evaluations
                final_report
        """

        self._validate_evaluate_inputs(
            role=role,
            skills=skills,
            experience=experience,
            questions=questions,
            answers=answers,
        )

        evaluations = []

        try:
            for question, answer in zip(questions, answers):
                logger.info("Evaluating answer...")

                evaluation = self.answer_evaluator.evaluate_answer(
                    question=question,
                    answer=answer,
                )

                evaluations.append(evaluation)

            logger.info("Generating final report...")

            report = self.report_generator.generate_report(
                role=role,
                skills=skills,
                experience=experience,
                questions=questions,
                answers=answers,
                evaluations=evaluations,
            )

            return {
                "questions": questions,
                "answers": answers,
                "evaluations": evaluations,
                "final_report": report,
            }

        except Exception as e:
            logger.exception("Interview evaluation failed.")
            raise RuntimeError(
                f"Interview evaluation failed: {e}"
            ) from e

    def _validate_evaluate_inputs(
        self,
        role: str,
        skills: str,
        experience: str,
        questions: list[str],
        answers: list[str],
    ) -> None:
        """
        Validate inputs for evaluate_interview.
        """

        # Validate role, skills, and experience
        if not role.strip():
            logger.error("Role is empty.")
            raise ValueError("Role cannot be empty.")

        if not skills.strip():
            logger.error("Skills are empty.")
            raise ValueError("Skills cannot be empty.")

        if not experience.strip():
            logger.error("Experience is empty.")
            raise ValueError("Experience cannot be empty.")

        # Validate question and answer lists
        if not questions:
            logger.error("Questions list is empty.")
            raise ValueError("Questions cannot be empty.")

        if not answers:
            logger.error("Answers list is empty.")
            raise ValueError("Answers cannot be empty.")

        # Validate list sizes
        if len(questions) != 5:
            logger.error(
                "Questions list contains %d items instead of 5.",
                len(questions),
            )
            raise ValueError("There must be exactly 5 questions.")

        if len(answers) != 5:
            logger.error(
                "Answers list contains %d items instead of 5.",
                len(answers),
            )
            raise ValueError("There must be exactly 5 answers.")

        # Validate each question
        for index, question in enumerate(questions, start=1):
            if not question.strip():
                logger.error("Question %d is empty.", index)
                raise ValueError(
                    f"Question {index} cannot be empty."
                )

        # Validate each answer
        for index, answer in enumerate(answers, start=1):
            if not answer.strip():
                logger.error("Answer %d is empty.", index)
                raise ValueError(
                    f"Answer {index} cannot be empty."
                )