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

                workbook_sheets = [s.strip().lower() for s in self.workbook.sheetnames]
                passed = sheet_name.strip().lower() in workbook_sheets

            # -----------------------------
            # 2️⃣ Cell Formula Validation
            # -----------------------------
            elif rule_type == "cell_formula_validation":

                sheet_name = config.get("sheet") or config.get("sheet_name")
                cell_address = config["cell"]
                required_functions = config.get("required_functions", [])
                reject_hardcoded = config.get("reject_hardcoded", False)

                if sheet_name in self.workbook.sheetnames:

                    sheet = self.workbook[sheet_name]
                    cell_value = sheet[cell_address].value

                    if isinstance(cell_value, str) and cell_value.startswith("="):

                        formula_upper = cell_value.upper()

                        functions_ok = all(
                            func.upper() in formula_upper
                            for func in required_functions
                        )

                        passed = functions_ok
                    else:
                        passed = False

            # -----------------------------
            # 3️⃣ Column Formula Validation
            # -----------------------------
            elif rule_type == "column_formula_validation":

                sheet_name = config["sheet"]
                column_letter = config["column_letter"]
                start_row = config["start_row"]
                required_functions = config.get("required_functions", [])
                reject_hardcoded = config.get("reject_hardcoded", False)

                if sheet_name in self.workbook.sheetnames:

                    sheet = self.workbook[sheet_name]
                    debug_passed = True

                    for r in range(start_row, sheet.max_row + 1):

                        cell = sheet[f"{column_letter}{r}"]

                        if not cell.value:
                            debug_passed = False
                            break

                        formula = str(cell.value).upper()

                        if not formula.startswith("="):
                            debug_passed = False
                            break

                        for func in required_functions:
                            if func.upper() not in formula:
                                debug_passed = False
                                break

                        if not debug_passed:
                            break

                    passed = debug_passed

            # -----------------------------
            # Result Builder
            # -----------------------------
            results.append({
                "id": check["id"],
                "section": check["section"],
                "status": "pass" if passed else "fail",
                "marks_awarded": check["marks"] if passed else 0,
                "max_marks": check["marks"],
                "debug_passed": passed
            })

        return results