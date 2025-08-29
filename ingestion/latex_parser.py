import re

def latex_to_text(latex_str: str) -> str:
    """
    Converts LaTeX source to plain text, excluding equations, comments,
    LaTeX commands, and section headings.
    """
    # Remove displayed equations
    text = re.sub(r"\$\$.*?\$\$", "", latex_str, flags=re.DOTALL)
    # Remove inline math
    text = re.sub(r"\$.*?\$", "", text)
    # Remove comments
    text = re.sub(r"%.*", "", text)
    # Remove section commands (\section, \subsection, etc.)
    text = re.sub(r"\\(sub)*section\*?\{.*?\}", "", text)
    # Remove other LaTeX commands
    text = re.sub(r"\\[a-zA-Z]+\{.*?\}", "", text)
    text = re.sub(r"\\[a-zA-Z]+", "", text)
    # Replace multiple spaces/newlines with a single space
    text = re.sub(r"\s+", " ", text)
    return text.strip()
