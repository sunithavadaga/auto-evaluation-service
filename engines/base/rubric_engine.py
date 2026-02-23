class RubricEngine:

    def __init__(self, rule_results, passing_percentage=50):
        self.rule_results = rule_results
        self.passing_percentage = passing_percentage

    def generate_report(self):

        section_scores = {}
        total_score = 0
        max_score = 0

        for result in self.rule_results:
            section = result["section"]
            marks_awarded = result["marks_awarded"]
            max_marks = result["max_marks"]

            if section not in section_scores:
                section_scores[section] = 0

            section_scores[section] += marks_awarded
            total_score += marks_awarded
            max_score += max_marks

        percentage = (total_score / max_score) * 100 if max_score > 0 else 0
        pass_status = percentage >= self.passing_percentage

        return {
            "section_scores": section_scores,
            "total_score": total_score,
            "max_score": max_score,
            "percentage": round(percentage, 2),
            "pass": pass_status,
            "details": self.rule_results
        }