from engines.excel.excel_engine import ExcelEngine


def get_engine(assignment_type, file_path, rules):

    if assignment_type == "excel":
        return ExcelEngine(file_path, rules)

    raise ValueError("Unsupported assignment type")