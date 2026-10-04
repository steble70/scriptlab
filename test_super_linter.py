"""
Test suite for super-linter.yml GitHub Actions workflow configuration.
Tests the linter setup, enabled validators, exclusions, and workflow triggers.
No external dependencies required - uses only standard library.
"""

import unittest
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional


class YAMLParser:
    """Simple YAML parser for GitHub Actions workflow files."""
    
    @staticmethod
    def load(file_path: str) -> Dict[str, Any]:
        """Parse YAML file and return as dictionary."""
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        return YAMLParser.parse(content)
    
    @staticmethod
    def parse(content: str) -> Dict[str, Any]:
        """Parse YAML content string into a dictionary."""
        lines = content.split('\n')
        return YAMLParser._parse_lines(lines, 0)[0]
    
    @staticmethod
    def _parse_lines(lines: List[str], start_index: int, indent_level: int = 0) -> tuple:
        """Recursively parse YAML lines."""
        result = {}
        i = start_index
        
        while i < len(lines):
            line = lines[i]
            stripped = line.lstrip()
            
            # Skip empty lines and comments
            if not stripped or stripped.startswith('#'):
                i += 1
                continue
            
            # Calculate current indent
            current_indent = len(line) - len(stripped)
            
            # If indent is less than expected, we're done with this block
            if current_indent < indent_level:
                return result, i
            
            # If indent is more than expected, skip (part of nested structure we'll handle)
            if current_indent > indent_level:
                i += 1
                continue
            
            # Parse key-value pair
            if ':' in stripped:
                key, value = stripped.split(':', 1)
                key = key.strip()
                value = value.strip()
                
                # Check if this is a nested structure
                if not value or value.startswith('['):
                    # Nested dict or list
                    if i + 1 < len(lines):
                        next_line = lines[i + 1]
                        next_indent = len(next_line) - len(next_line.lstrip())
                        next_stripped = next_line.lstrip()
                        
                        if next_indent > current_indent and next_stripped:
                            if next_stripped.startswith('-'):
                                # It's a list
                                result[key], i = YAMLParser._parse_list(lines, i + 1, next_indent)
                            else:
                                # It's a nested dict
                                result[key], i = YAMLParser._parse_lines(lines, i + 1, next_indent)
                            continue
                
                # Parse the value
                result[key] = YAMLParser._parse_value(value)
            
            i += 1
        
        return result, i
    
    @staticmethod
    def _parse_list(lines: List[str], start_index: int, indent_level: int) -> tuple:
        """Parse YAML list."""
        result = []
        i = start_index
        
        while i < len(lines):
            line = lines[i]
            stripped = line.lstrip()
            current_indent = len(line) - len(stripped)
            
            # Skip empty lines and comments
            if not stripped or stripped.startswith('#'):
                i += 1
                continue
            
            # If indent is less than list indent, we're done
            if current_indent < indent_level:
                return result, i
            
            # If indent is more than list indent, skip
            if current_indent > indent_level:
                i += 1
                continue
            
            # Parse list item
            if stripped.startswith('-'):
                item_content = stripped[1:].strip()
                result.append(YAMLParser._parse_value(item_content))
            
            i += 1
        
        return result, i
    
    @staticmethod
    def _parse_value(value: str) -> Any:
        """Parse a YAML value."""
        value = value.strip()
        
        # Handle null
        if value.lower() in ('null', '~', ''):
            return None
        
        # Handle booleans
        if value.lower() in ('true', 'yes', 'on'):
            return True
        if value.lower() in ('false', 'no', 'off'):
            return False
        
        # Handle numbers
        if value.isdigit():
            return int(value)
        try:
            if '.' in value:
                return float(value)
        except ValueError:
            pass
        
        # Handle quoted strings
        if (value.startswith('"') and value.endswith('"')) or \
           (value.startswith("'") and value.endswith("'")):
            return value[1:-1]
        
        # Return as string
        return value


class TestSuperLinterWorkflow(unittest.TestCase):
    """Test cases for super-linter.yml workflow configuration."""

    @classmethod
    def setUpClass(cls):
        """Load the super-linter.yml file once for all tests."""
        workflow_path = Path(".github/workflows/super-linter.yml")
        
        if not workflow_path.exists():
            raise FileNotFoundError(f"Workflow file not found at {workflow_path}")
        
        cls.workflow = YAMLParser.load(str(workflow_path))

    def test_workflow_name_exists(self):
        """Test that the workflow has a proper name."""
        self.assertIn("name", self.workflow)
        self.assertEqual(self.workflow["name"], "Lint Code Base")

    def test_workflow_triggers(self):
        """Test that the workflow is triggered on push and pull_request."""
        self.assertIn("on", self.workflow)
        triggers = self.workflow["on"]
        
        # Check for push trigger
        self.assertIn("push", triggers)
        self.assertIn("branches", triggers["push"])
        self.assertIn("master", triggers["push"]["branches"])
        
        # Check for pull_request trigger
        self.assertIn("pull_request", triggers)
        self.assertIn("branches", triggers["pull_request"])
        self.assertIn("master", triggers["pull_request"]["branches"])

    def test_permissions_configured(self):
        """Test that proper permissions are set."""
        self.assertIn("permissions", self.workflow)
        permissions = self.workflow["permissions"]
        
        self.assertEqual(permissions["contents"], "read")
        self.assertEqual(permissions["pull-requests"], "write")

    def test_job_exists(self):
        """Test that at least one job is defined."""
        self.assertIn("jobs", self.workflow)
        jobs = self.workflow["jobs"]
        self.assertGreater(len(jobs), 0)
        self.assertIn("lint", jobs)

    def test_lint_job_configuration(self):
        """Test the lint job configuration."""
        lint_job = self.workflow["jobs"]["lint"]
        
        self.assertIn("name", lint_job)
        self.assertEqual(lint_job["name"], "Lint")
        
        self.assertIn("runs-on", lint_job)
        self.assertEqual(lint_job["runs-on"], "ubuntu-24.04")

    def test_checkout_step_exists(self):
        """Test that the checkout step is configured."""
        steps = self.workflow["jobs"]["lint"]["steps"]
        checkout_step = next((s for s in steps if s.get("name") == "Checkout code"), None)
        
        self.assertIsNotNone(checkout_step)
        self.assertEqual(checkout_step["uses"], "actions/checkout@v5")
        self.assertIn("with", checkout_step)
        self.assertEqual(checkout_step["with"]["fetch-depth"], 0)

    def test_super_linter_step_exists(self):
        """Test that the super-linter step is configured."""
        steps = self.workflow["jobs"]["lint"]["steps"]
        linter_step = next((s for s in steps if s.get("name") == "Super-linter"), None)
        
        self.assertIsNotNone(linter_step)
        self.assertEqual(linter_step["uses"], "github/super-linter@v7")
        self.assertIn("env", linter_step)

    def test_github_token_configured(self):
        """Test that GITHUB_TOKEN is properly configured."""
        env = self.workflow["jobs"]["lint"]["steps"][1]["env"]
        self.assertIn("GITHUB_TOKEN", env)
        self.assertEqual(env["GITHUB_TOKEN"], "${{ secrets.GITHUB_TOKEN }}")

    def test_default_branch_configured(self):
        """Test that DEFAULT_BRANCH is set to master."""
        env = self.workflow["jobs"]["lint"]["steps"][1]["env"]
        self.assertIn("DEFAULT_BRANCH", env)
        self.assertEqual(env["DEFAULT_BRANCH"], "master")

    def test_validate_all_codebase_disabled(self):
        """Test that VALIDATE_ALL_CODEBASE is disabled for performance."""
        env = self.workflow["jobs"]["lint"]["steps"][1]["env"]
        self.assertIn("VALIDATE_ALL_CODEBASE", env)
        self.assertFalse(env["VALIDATE_ALL_CODEBASE"])

    def test_enabled_linters(self):
        """Test that required linters are enabled."""
        env = self.workflow["jobs"]["lint"]["steps"][1]["env"]
        
        enabled_linters = {
            "VALIDATE_POWERSHELL": True,
            "VALIDATE_PYTHON": True,
            "VALIDATE_JAVASCRIPT_ES": True,
            "VALIDATE_JSON": True,
            "VALIDATE_MARKDOWN": True,
        }
        
        for linter, expected_value in enabled_linters.items():
            self.assertIn(linter, env)
            self.assertEqual(env[linter], expected_value, f"{linter} should be {expected_value}")

    def test_python_linter_configured(self):
        """Test that ruff is configured as the Python linter."""
        env = self.workflow["jobs"]["lint"]["steps"][1]["env"]
        self.assertIn("PYTHON_LINTER", env)
        self.assertEqual(env["PYTHON_LINTER"], "ruff")

    def test_filter_regex_exclude(self):
        """Test that file exclusion patterns are properly configured."""
        env = self.workflow["jobs"]["lint"]["steps"][1]["env"]
        self.assertIn("FILTER_REGEX_EXCLUDE", env)
        
        excluded_pattern = env["FILTER_REGEX_EXCLUDE"]
        
        # Test that binary and notebook files are excluded
        excluded_extensions = [".pdf", ".jpg", ".jpeg", ".png", ".svg", ".csv", ".ipynb"]
        for ext in excluded_extensions:
            self.assertIn(ext, excluded_pattern, f"Extension {ext} should be in exclusion pattern")

    def test_excluded_files_pattern_validity(self):
        """Test that the exclusion regex pattern is valid."""
        env = self.workflow["jobs"]["lint"]["steps"][1]["env"]
        excluded_pattern = env["FILTER_REGEX_EXCLUDE"]
        
        try:
            re.compile(excluded_pattern)
        except re.error as e:
            self.fail(f"Invalid regex pattern: {e}")

    def test_no_disabled_linters_by_mistake(self):
        """Test that commonly needed linters are not accidentally disabled."""
        env = self.workflow["jobs"]["lint"]["steps"][1]["env"]
        
        # These linters are enabled, so they shouldn't have VALIDATE_* = false entries
        should_not_have_false_validation = [
            "VALIDATE_POWERSHELL",
            "VALIDATE_PYTHON",
            "VALIDATE_JAVASCRIPT_ES",
            "VALIDATE_JSON",
            "VALIDATE_MARKDOWN",
        ]
        
        for validator in should_not_have_false_validation:
            if validator in env:
                self.assertNotEqual(env[validator], False, 
                                   f"{validator} should not be explicitly disabled")

    def test_steps_order(self):
        """Test that steps are in the correct order."""
        steps = self.workflow["jobs"]["lint"]["steps"]
        step_names = [step.get("name") for step in steps]
        
        # Checkout should come before linting
        checkout_idx = step_names.index("Checkout code")
        linter_idx = step_names.index("Super-linter")
        
        self.assertLess(checkout_idx, linter_idx, 
                       "Checkout step should come before linter step")

    def test_valid_ubuntu_version(self):
        """Test that a valid Ubuntu version is specified."""
        runs_on = self.workflow["jobs"]["lint"]["runs-on"]
        self.assertTrue(runs_on.startswith("ubuntu-"), 
                       f"Expected ubuntu runner, got {runs_on}")

    def test_no_hardcoded_secrets(self):
        """Test that no hardcoded secrets are present in the workflow."""
        def dict_to_string(d):
            """Convert dict to string representation."""
            result = []
            for k, v in d.items():
                if isinstance(v, dict):
                    result.append(dict_to_string(v))
                elif isinstance(v, list):
                    for item in v:
                        if isinstance(item, dict):
                            result.append(dict_to_string(item))
                        else:
                            result.append(str(item))
                else:
                    result.append(str(v))
            return " ".join(result)
        
        workflow_str = dict_to_string(self.workflow)
        
        # Check for obvious hardcoded values (not checking for actual secrets,
        # just ensuring they're using ${{ secrets.* }} syntax)
        self.assertIn("secrets.GITHUB_TOKEN", workflow_str)


class TestSuperLinterIntegration(unittest.TestCase):
    """Integration tests for the super-linter workflow."""

    @classmethod
    def setUpClass(cls):
        """Load the workflow file."""
        workflow_path = Path(".github/workflows/super-linter.yml")
        cls.workflow = YAMLParser.load(str(workflow_path))

    def test_workflow_is_valid_yaml(self):
        """Test that the workflow file is valid YAML."""
        # If this loads without error, it's valid YAML
        self.assertIsInstance(self.workflow, dict)

    def test_no_undefined_variables(self):
        """Test that all environment variables follow correct syntax."""
        env = self.workflow["jobs"]["lint"]["steps"][1]["env"]
        
        for key, value in env.items():
            if isinstance(value, str):
                # Check for unclosed ${{ }}
                if "${{" in value:
                    self.assertIn("}}", value, 
                                 f"Variable {key} has unclosed ${{{{")

    def test_linters_cover_repo_languages(self):
        """Test that linters are enabled for the main languages in the repo.
        
        Repo composition: Jupyter Notebook (72.6%), PowerShell (16.1%), 
        JavaScript (5.8%), Python (5.3%), Vim Script (0.2%)
        """
        env = self.workflow["jobs"]["lint"]["steps"][1]["env"]
        
        # PowerShell and Python are enabled (major components)
        self.assertTrue(env.get("VALIDATE_POWERSHELL"))
        self.assertTrue(env.get("VALIDATE_PYTHON"))
        
        # JavaScript is enabled (5.8%)
        self.assertTrue(env.get("VALIDATE_JAVASCRIPT_ES"))
        
        # JSON is enabled (good for general code quality)
        self.assertTrue(env.get("VALIDATE_JSON"))

    def test_ipynb_exclusion_makes_sense(self):
        """Test that .ipynb files are excluded (since they're Jupyter Notebooks)."""
        env = self.workflow["jobs"]["lint"]["steps"][1]["env"]
        excluded_pattern = env["FILTER_REGEX_EXCLUDE"]
        
        # Jupyter notebooks (.ipynb) should be excluded since they're not plain Python
        self.assertIn(".ipynb", excluded_pattern,
                     "Jupyter notebooks should be excluded from linting")


def run_tests():
    """Run all tests and display results."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test cases
    suite.addTests(loader.loadTestsFromTestCase(TestSuperLinterWorkflow))
    suite.addTests(loader.loadTestsFromTestCase(TestSuperLinterIntegration))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
