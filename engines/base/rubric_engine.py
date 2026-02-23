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
            marks_awarded = result["marks"]

            # Calculate section score
            if section not in section_scores:
                section_scores[section] = 0

            section_scores[section] += marks_awarded

            total_score += marks_awarded

        # Calculate maximum possible marks
        for result in self.rule_results:
            max_score += result.get("max_marks", result["marks"] if result["passed"] else result.get("max_marks", 0))

        # If max_marks not provided, assume sum of all marks
        if max_score == 0:
            max_score = sum(r["marks"] for r in self.rule_results)

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