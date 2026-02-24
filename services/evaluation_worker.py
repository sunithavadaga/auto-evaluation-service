from sqlalchemy.orm import Session
from services.models import Submission
from engines.engine_factory import get_engine
from engines.base.rubric_engine import RubricEngine
import json


def process_pending_submissions(db: Session):

    pending = db.query(Submission).filter(
        Submission.status == "submitted"
    ).all()

    for submission in pending:

        try:
            file_path = submission.submission_link

            with open("assignments/excel_101/rules.json") as f:
                rules = json.load(f)

            engine = get_engine(rules["assignment_type"], file_path, rules)
            rule_results = engine.evaluate()

            rubric = RubricEngine(rule_results)
            final_report = rubric.generate_report()

            submission.score = final_report["total_score"]
            submission.max_score = final_report["max_score"]
            submission.percentage = final_report["percentage"]
            submission.feedback = "\n".join(final_report.get("feedback", []))
            submission.evaluation_details = final_report["detailed_results"]
            submission.status = "evaluated"

        except Exception as e:
            submission.status = "failed"
            submission.feedback = str(e)

    db.commit()