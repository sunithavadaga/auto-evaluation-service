import openpyxl
from openpyxl import load_workbook
from engines.base.rule_executor import RuleExecutor


class ExcelEngine:

    def __init__(self, file_path, rules):
        self.file_path = file_path
        self.rules = rules
        self.workbook = openpyxl.load_workbook(
            file_path,
            data_only=False  # Important: Keep formulas
        )

    def evaluate(self):
        executor = RuleExecutor(self.workbook)
        results = executor.execute(self.rules["checks"])
        return results