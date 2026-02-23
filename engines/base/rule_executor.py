class RuleExecutor:

    def __init__(self, workbook):
        self.workbook = workbook

    def execute(self, checks):

        results = []

        for check in checks:

            passed = False
            rule_type = check["type"]
            config = check["config"]

            # -----------------------------
            # 1️⃣ Sheet Exists
            # -----------------------------
            if rule_type == "sheet_exists":
                sheet_name = config.get("sheet") or config.get("sheet_name")
                passed = sheet_name in self.workbook.sheetnames

            # -----------------------------
            # 2️⃣ Cell Formula Validation
            # -----------------------------
            elif rule_type == "cell_formula_validation":
                sheet_name = config["sheet"]
                cell_address = config["cell"]
                required_functions = config.get("required_functions", [])
                reject_hardcoded = config.get("reject_hardcoded", False)

                if sheet_name in self.workbook.sheetnames:
                    sheet = self.workbook[sheet_name]
                    cell_value = sheet[cell_address].value

                    if isinstance(cell_value, str) and cell_value.startswith("="):

                        formula_upper = cell_value.upper()

                        # Check required functions
                        functions_ok = all(
                            func.upper() in formula_upper
                            for func in required_functions
                        )

                        # Reject hardcoded values
                        if reject_hardcoded:
                            passed = functions_ok
                        else:
                            passed = True
                    else:
                        passed = False

            # -----------------------------
            # 3️⃣ Column Formula Validation
            # -----------------------------
            elif rule_type == "column_formula_validation":
                sheet_name = config["sheet"]
                column_letter = config["column_letter"]
                start_row = config.get("start_row", 2)
                required_functions = config.get("required_functions", [])
                reject_hardcoded = config.get("reject_hardcoded", False)

                if sheet_name in self.workbook.sheetnames:
                    sheet = self.workbook[sheet_name]
                    passed = True

                    for row in range(start_row, sheet.max_row + 1):
                        cell_value = sheet[f"{column_letter}{row}"].value

                        if isinstance(cell_value, str) and cell_value.startswith("="):
                            formula_upper = cell_value.upper()

                            functions_ok = all(
                                func.upper() in formula_upper
                                for func in required_functions
                            )

                            if not functions_ok:
                                passed = False
                                break
                        else:
                            if reject_hardcoded:
                                passed = False
                                break
                else:
                    passed = False

            # -----------------------------
            # Result Builder
            # -----------------------------
            results.append({
                "id": check["id"],
                "section": check["section"],
                "status": "pass" if passed else "fail",
                "marks_awarded": check["marks"] if passed else 0,
                "max_marks": check["marks"]
            })

        return results