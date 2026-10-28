"""Dependency-free checks for NEX documentation consistency."""
import ast
import re
import unittest
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = {"agent-spec.md", "system-instructions.md", "tool-manifest.md", "test-plan.md", "setup.md", "checkpoint.md"}
LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
FENCE = re.compile(r"^\s*(`{3,}|~{3,})")


def without_fences(text):
    lines, fence, size = [], None, 0
    for line in text.splitlines():
        match = FENCE.match(line)
        if match:
            mark = match.group(1)
            if fence is None:
                fence, size = mark[0], len(mark)
            elif mark[0] == fence and len(mark) >= size:
                fence, size = None, 0
            continue
        if fence is None:
            lines.append(line)
    return "\n".join(lines)


class DocumentationConsistencyTests(unittest.TestCase):
    def test_relative_markdown_links_resolve(self):
        files = sorted(ROOT.rglob("*.md"))
        self.assertTrue(files, "No Markdown files found")
        failures = []
        for source in files:
            content = without_fences(source.read_text(encoding="utf-8"))
            for match in LINK.finditer(content):
                target = match.group(1).strip().split()[0].strip("<>")
                parsed = urlsplit(target)
                if parsed.scheme or parsed.netloc or target.startswith("#"):
                    continue
                path = unquote(parsed.path)
                if path and not (source.parent / path).resolve().exists():
                    failures.append(f"{source.relative_to(ROOT)}: {target}")
        self.assertEqual(failures, [], "Broken relative Markdown links:\n" + "\n".join(failures))

    def test_generator_artifacts_match_specification(self):
        source = ROOT / "scripts" / "agent_factory.py"
        spec = ROOT / "docs" / "agent-factory-spec.md"
        self.assertTrue(source.is_file(), "Agent Factory source missing")
        self.assertTrue(spec.is_file(), "Agent Factory specification missing")
        module = ast.parse(source.read_text(encoding="utf-8"))
        render = next(n for n in module.body if isinstance(n, ast.FunctionDef) and n.name == "render")
        returned = next(n.value for n in ast.walk(render) if isinstance(n, ast.Return) and isinstance(n.value, ast.Dict))
        actual = {k.value for k in returned.keys if isinstance(k, ast.Constant) and isinstance(k.value, str)}
        self.assertEqual(actual, ARTIFACTS)
        spec_text = spec.read_text(encoding="utf-8")
        documented = {name for name in ARTIFACTS if f"`{name}`" in spec_text}
        self.assertEqual(documented, ARTIFACTS, "Spec output names differ from generator output names")


if __name__ == "__main__":
    unittest.main()
