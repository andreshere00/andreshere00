from pathlib import Path

from docx import Document

EXAMPLES_DIR = "examples"

AGREEMENT_V1 = [
    "This Service Agreement is made between Acme Corp and Globex Ltd.",
    "The Supplier will deliver the software platform by 30 June 2027.",
    "The total fee is 10,000 EUR, payable within 30 days of invoice.",
    "Either party may terminate this agreement with 60 days written notice.",
    "The Supplier keeps all customer data confidential for the duration of the agreement.",
    "Liability of the Supplier is limited to the fees paid in the last 12 months.",
    "This agreement is governed by the laws of Spain.",
]
AGREEMENT_V2 = [
    "This Service Agreement is made between Acme Corp and Globex Ltd.",
    "The Supplier will deliver the software platform by 30 September 2027.",
    "The total fee is 12,500 EUR, payable within 45 days of invoice.",
    "Either party may terminate this agreement with 90 days written notice.",
    "The Supplier keeps all customer data confidential for the duration of the agreement.",
    "Liability of the Supplier is limited to the fees paid in the last 12 months.",
    "This agreement is governed by the laws of Spain.",
]
AGREEMENT_V3 = [
    "This Service Agreement is made between Acme Corp and Globex Ltd.",
    "The Supplier will deliver the software platform by 30 September 2027.",
    "The total fee is 12,500 EUR, payable within 45 days of invoice.",
    "Late payments accrue interest of 2% per month.",
    "Either party may terminate this agreement with 90 days written notice.",
    "The Supplier keeps all customer data confidential for five years after termination.",
    "Liability of the Supplier is limited to the fees paid in the last 12 months.",
]

NOTES_V1 = [
    "Attendees: Ana, Luis, Marta.",
    "Decision: launch the beta on 15 March.",
    "Action: Luis prepares the release checklist by Friday.",
    "Action: Marta books the demo room.",
    "Risk: the payment provider has not confirmed the sandbox keys.",
]
NOTES_V2 = [
    "Attendees: Ana, Luis, Marta, Pedro.",
    "Decision: launch the beta on 22 March.",
    "Action: Luis prepares the release checklist by Thursday.",
    "Action: Pedro confirms the payment provider sandbox keys.",
    "Risk: the payment provider has not confirmed the sandbox keys.",
]

POLICY_V1 = [
    "We collect your name and email address to create your account.",
    "We keep your data for 12 months after you close your account.",
    "We never share personal data with third parties.",
]

EXAMPLES: dict[str, tuple[str, list[str], list[tuple[str, str]]]] = {
    "service-agreement.v1.docx": ("Service Agreement", AGREEMENT_V1, [("Monthly fee", "10000")]),
    "service-agreement.v2.docx": ("Service Agreement", AGREEMENT_V2, [("Monthly fee", "12500")]),
    "service-agreement.v3.docx": ("Service Agreement", AGREEMENT_V3, [("Monthly fee", "12500")]),
    "meeting-notes.v1.docx": ("Product meeting", NOTES_V1, []),
    "meeting-notes.v2.docx": ("Product meeting", NOTES_V2, []),
    "privacy-policy.v1.docx": ("Privacy policy", POLICY_V1, []),
    "privacy-policy.v1-copy.docx": ("Privacy policy", POLICY_V1, []),
}


def seed_examples(workspace: Path) -> list[Path]:
    """Writes the sample Word documents into `<workspace>/examples/`.

    Args:
        workspace: The agent workspace directory.

    Returns:
        Paths of the documents that were created. Existing files are left untouched.
    """
    target = workspace / EXAMPLES_DIR
    target.mkdir(parents=True, exist_ok=True)
    created: list[Path] = []
    for name, (heading, paragraphs, rows) in EXAMPLES.items():
        path = target / name
        if path.exists():
            continue
        document = Document()
        document.add_heading(heading, level=1)
        for text in paragraphs:
            document.add_paragraph(text)
        if rows:
            table = document.add_table(rows=len(rows), cols=2)
            for row, (key, value) in zip(table.rows, rows, strict=True):
                row.cells[0].text, row.cells[1].text = key, value
        document.save(str(path))
        created.append(path)
    return created
