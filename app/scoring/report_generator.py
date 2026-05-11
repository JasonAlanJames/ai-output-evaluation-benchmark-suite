from typing import List

from app.schemas import EvaluationResult


def generate_markdown_report(results: List[EvaluationResult]) -> str:
    total_cases = len(results)
    passed_cases = sum(1 for result in results if result.passed)
    failed_cases = total_cases - passed_cases
    average_score = round(
        sum(result.score for result in results) / total_cases,
        2,
    ) if total_cases else 0.0

    lines = [
        "# AI Output Evaluation Report",
        "",
        f"Total Cases: {total_cases}",
        f"Passed Cases: {passed_cases}",
        f"Failed Cases: {failed_cases}",
        f"Average Score: {average_score}",
        "",
        "## Results",
        "",
    ]

    for index, result in enumerate(results, start=1):
        lines.extend([
            f"### Case {index}: {result.category}",
            "",
            f"Passed: {result.passed}",
            f"Score: {result.score}",
            "",
            "Findings:",
        ])

        for finding in result.findings:
            lines.append(f"- {finding}")

        lines.append("")
        lines.append("Recommendations:")

        if result.recommendations:
            for recommendation in result.recommendations:
                lines.append(f"- {recommendation}")
        else:
            lines.append("- No recommendations. Output met evaluation expectations.")

        lines.append("")

    return "\n".join(lines)