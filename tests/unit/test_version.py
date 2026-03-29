import os
import re

def test_version_match():
    """Check if version in .version matches version in __init__.py"""
    with open(".version", "r") as f:
        version = f.read().strip()

    # Enforce no '-pre' on main branch releases
    # GITHUB_REF_NAME is provided by GitHub Actions
    if os.environ.get('GITHUB_REF_NAME') == 'main':
        assert "-pre" not in version, "Release error: .version file on 'main' branch must not contain '-pre'!"

    with open("__init__.py", "r") as f:
        content = f.read()
        # Support both single and double quotes for the version string
        pattern = rf'version_string\s*=\s*[\'"]{re.escape(version)}[\'"]'
        assert re.search(pattern, content), f"Version string '{version}' not found in __init__.py"

def test_version_tuple_match():
    """Check if version in .version matches version tuple in __init__.py"""
    with open(".version", "r") as f:
        version = f.read().strip()

    # Strip any suffix like -pre or -dev for the numeric tuple
    # This matches the logic in our Makefile
    numeric_version = version.split("-")[0]
    parts = numeric_version.split(".")
    
    # format (0, 8, 0)
    version_tuple = f"({', '.join(parts)})"

    with open("__init__.py", "r") as f:
        content = f.read()
        expected = f"version = {version_tuple}"
        assert expected in content, f"Expected {expected} not found in __init__.py"
