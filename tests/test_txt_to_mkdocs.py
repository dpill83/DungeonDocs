"""
Smoke test: convert only the Acolyte background txt and assert Benefits table and Equipment format.
Run from repo root: pytest tests/test_txt_to_mkdocs.py -v
"""
import sys
from pathlib import Path

import pytest

# Import the converter from the single source of truth
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))
import txt_to_mkdocs  # noqa: E402

convert_file = txt_to_mkdocs.convert_file


def test_acolyte_conversion_produces_benefits_table_and_equipment_list():
    """Convert Acolyte txt only; assert output has Benefits table and Equipment <ul>."""
    docs_root = REPO_ROOT / "docs"
    txt_path = REPO_ROOT / "scraped-dnd2024" / "dnd2024-wikidot-com-background-acolyte.txt"
    if not txt_path.exists():
        pytest.skip(f"Scraped file not found: {txt_path}")

    result = convert_file(txt_path, docs_root)
    assert result is not None, "convert_file should return the output path"

    expected_path = docs_root / "dnd2024" / "backgrounds" / "acolyte.md"
    assert result == expected_path, f"Output should be written to {expected_path}"

    content = result.read_text(encoding="utf-8")

    assert "## Benefits\n\n| Feature" in content, (
        "Output must contain '## Benefits' followed by a blank line and the table header"
    )
    assert "<ul>" in content, "Equipment A/B must be rendered as HTML list (<ul>)"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
