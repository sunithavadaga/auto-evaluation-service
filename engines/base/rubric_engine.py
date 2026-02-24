class RubricEngine:

    def __init__(self, rule_results, passing_percentage=50):
        self.rule_results = rule_results
        self.passing_percentage = passing_percentage

    def generate_report(self):

        total_score = 0
        max_score = 0
        feedback = []

        for result in self.rule_results:
            total_score += result["marks_awarded"]
            max_score += result["max_marks"]

            if result["status"] == "fail":
                feedback.append(f"{result['id']} failed")

        percentage = (total_score / max_score) * 100 if max_score > 0 else 0

        final_status = "Pass" if percentage >= self.passing_percentage else "Fail"

        return {
            "total_score": total_score,
            "max_score": max_score,
            "percentage": round(percentage, 2),
            "status": final_status,
            "feedback": feedback,
            "detailed_results": self.rule_results
        }