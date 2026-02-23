class RuleExecutor:

    def __init__(self, workbook):
        self.workbook = workbook

    def execute(self, checks):

        results = []

        for check in checks:

            passed = False

            if check["type"] == "sheet_exists":
                sheet_name = check["config"]["sheet"]
                passed = sheet_name in self.workbook.sheetnames

            elif check["type"] == "column_exists":
                sheet_name = check["config"]["sheet"]
                column_name = check["config"]["column"]

                if sheet_name in self.workbook.sheetnames:
                    sheet = self.workbook[sheet_name]
                    headers = [cell.value for cell in sheet[1]]
                    passed = column_name in headers

            # 🔥 NEW FORMULA RULE
            elif check["type"] == "cell_formula_contains":
                sheet_name = check["config"]["sheet"]
                cell_address = check["config"]["cell"]
                must_contain = check["config"]["must_contain"]

                if sheet_name in self.workbook.sheetnames:
                    sheet = self.workbook[sheet_name]
                    cell_value = sheet[cell_address].value

                    if isinstance(cell_value, str):
                        passed = must_contain.upper() in cell_value.upper()
                    else:
                        passed = False
                else:
                    passed = False

            results.append({
                "id": check["id"],
                "section": check["section"],
                "passed": passed,
                "marks": check["marks"] if passed else 0,
                "max_marks": check["marks"]
            })

        return results