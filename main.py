import json
from fastapi import FastAPI
from engines.engine_factory import get_engine
from engines.base.rubric_engine import RubricEngine

app = FastAPI()

@app.post("/evaluate_excel")
def evaluate_excel():

    file_path = "uploads/sample.xlsx"

    with open("assignments/excel_101/rules.json") as f:
        rules = json.load(f)

    assignment_type = rules["assignment_type"]

    engine = get_engine(assignment_type, file_path, rules)
    rule_results = engine.evaluate()

    print("RULE RESULTS:", rule_results)

    rubric = RubricEngine(rule_results)
    final_report = rubric.generate_report()

    print("FINAL REPORT:", final_report)

    return final_report