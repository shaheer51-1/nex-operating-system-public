"""Local NEX skill installer and portable Agent Skills exporter."""
from __future__ import annotations

import argparse
import os
import re
import shutil
import sys
import tempfile
import time
import zipfile
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
CLIENTS = ("claude", "grok", "codex", "cursor")


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def destinations(scope: str, client: str, project: Path) -> Path:
    if scope == "project":
        return project / {
            "claude": Path(".claude/skills"),
            "grok": Path(".grok/skills"),
            "codex": Path(".agents/skills"),
            "cursor": Path(".agents/skills"),
        }[client]
    if client == "claude":
        return Path.home() / ".claude/skills"
    if client == "grok":
        return Path.home() / ".grok/skills"
    if client == "codex":
        return Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex"))).expanduser() / "skills"
    return Path.home() / ".cursor/skills"


def discover(root: Path) -> list[tuple[str, Path, str]]:
    base = root / ".agents/skills"
    if (root / ".agents").is_symlink() or base.is_symlink() or not base.resolve().is_relative_to(root.resolve()):
        raise ValueError("Skill folder must stay inside this repository.")
    if not base.is_dir():
        raise ValueError("Canonical skill folder .agents/skills was not found.")
    result = []
    for folder in sorted(base.iterdir(), key=lambda item: item.name):
        if folder.is_symlink() or not folder.is_dir():
            continue
        if not NAME_RE.fullmatch(folder.name):
            raise ValueError("Skill names must be lowercase letters, digits, and hyphens.")
        file = folder / "SKILL.md"
        if file.is_symlink() or not file.is_file():
            continue
        text = file.read_text(encoding="utf-8")
        parts = text.split("---", 2)
        if len(parts) != 3 or parts[0].strip():
            raise ValueError("Invalid YAML frontmatter in " + folder.name + "/SKILL.md.")
        name = re.search(r"(?m)^name:\s*([a-z0-9-]+)\s*$", parts[1])
        desc = re.search(r"(?m)^description:\s*(.+?)\s*$", parts[1])
        if not name or name.group(1) != folder.name or not desc:
            raise ValueError("Skill name and description must match its folder and metadata.")
        result.append((folder.name, folder, desc.group(1)))
    if not result:
        raise ValueError("No valid skills found.")
    return result


def package_files(folder: Path) -> list[Path]:
    files = []
    for current, dirs, names in os.walk(folder, followlinks=False):
        current_path = Path(current)
        for name in dirs:
            if (current_path / name).is_symlink():
                raise ValueError("Skill packages cannot contain symbolic links.")
        dirs.sort()
        for name in sorted(names):
            path = current_path / name
            if path.is_symlink() or not path.is_file():
                raise ValueError("Skill packages may contain regular files only.")
            files.append(path)
    return files


def same_tree(source: Path, target: Path) -> bool:
    if target.is_symlink() or not target.is_dir():
        return False
    left = {p.relative_to(source).as_posix(): p for p in package_files(source)}
    right = {p.relative_to(target).as_posix(): p for p in package_files(target)}
    return left.keys() == right.keys() and all(left[k].read_bytes() == right[k].read_bytes() for k in left)


def install_one(source: Path, target: Path, overwrite: bool) -> str:
    if target.is_symlink():
        raise ValueError("Refusing to write through a symbolic link: " + str(target))
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists() and same_tree(source, target):
        return "Already current: " + str(target)
    if target.exists() and not overwrite:
        raise FileExistsError("Different files already exist at " + str(target) + "; review them or use --overwrite.")
    stage_root = Path(tempfile.mkdtemp(prefix=".nex-skill-", dir=target.parent))
    staged = stage_root / target.name
    backup = None
    try:
        package_files(source)
        shutil.copytree(source, staged, symlinks=False)
        package_files(staged)
        if target.exists():
            backup = target.with_name(target.name + ".backup-" + str(int(time.time())))
            suffix = 1
            while backup.exists():
                backup = target.with_name(target.name + ".backup-" + str(int(time.time())) + "-" + str(suffix))
                suffix += 1
            target.rename(backup)
        staged.rename(target)
    except Exception:
        if backup and backup.exists() and not target.exists():
            backup.rename(target)
        raise
    finally:
        shutil.rmtree(stage_root, ignore_errors=True)
    result = "Installed: " + str(target)
    if backup:
        result += " (previous copy backed up to " + str(backup) + ")"
    return result


def selected(catalog: list[tuple[str, Path, str]], names: list[str]) -> list[tuple[str, Path, str]]:
    if not names:
        return catalog
    by_name = {entry[0]: entry for entry in catalog}
    missing = [name for name in names if name not in by_name]
    if missing:
        raise ValueError("Unknown skill(s): " + ", ".join(missing))
    return [by_name[name] for name in names]


def run_list(_: argparse.Namespace) -> int:
    for name, _, description in discover(repo_root()):
        print(name + " — " + description)
    return 0


def run_install(args: argparse.Namespace) -> int:
    root = repo_root()
    entries = selected(discover(root), args.skill)
    project = Path(args.project_root).expanduser().resolve() if args.project_root else Path.cwd().resolve()
    if not project.is_dir():
        raise ValueError("Project root must be an existing directory.")
    clients = CLIENTS if args.client == "all" else (args.client,)
    plan = {}
    for client in clients:
        folder = destinations(args.scope, client, project).resolve()
        for name, source, _ in entries:
            plan.setdefault(folder / name, source)
    conflicts = [
        str(target) for target, source in plan.items()
        if target.is_symlink() or (target.exists() and not same_tree(source, target) and not args.overwrite)
    ]
    if conflicts:
        raise FileExistsError(
            "No files were changed. Review these existing copies first: " + "; ".join(conflicts) +
            ". Use --overwrite only after reviewing; backups will be preserved."
        )
    for target, source in plan.items():
        print(install_one(source, target, args.overwrite))
    print("No network, model, API, or package-manager calls were made.")
    return 0


def run_export(args: argparse.Namespace) -> int:
    output = Path(args.output).expanduser().resolve()
    if output.exists():
        raise FileExistsError("Output already exists; choose another archive path.")
    entries = selected(discover(repo_root()), args.skill)
    output.parent.mkdir(parents=True, exist_ok=True)
    try:
        with zipfile.ZipFile(output, "x", compression=zipfile.ZIP_DEFLATED) as archive:
            archive.writestr(
                "README.txt",
                "NEX Agent Skills package\n\n"
                "Each skills/<name>/ folder contains a SKILL.md and optional supporting files.\n"
                "Copy or import a skill only in a client that supports the Agent Skills format.\n"
                "This archive does not configure client tools. Review each skill before enabling it.\n",
            )
            for name, folder, _ in entries:
                for path in package_files(folder):
                    archive.write(path, "skills/" + name + "/" + path.relative_to(folder).as_posix())
    except Exception:
        output.unlink(missing_ok=True)
        raise
    print("Created: " + str(output))
    print("The ZIP contains instructions only. It does not install software or configure tools.")
    return 0


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Install or export NEX skills using local files only.")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("list", help="List skills in the canonical NEX catalogue.")
    install = commands.add_parser("install", help="Copy skills to supported client folders.")
    install.add_argument("--client", choices=(*CLIENTS, "all"), required=True)
    install.add_argument("--scope", choices=("user", "project"), default="user")
    install.add_argument("--project-root", help="Existing target project; defaults to the current folder.")
    install.add_argument("--skill", action="append", default=[], help="Skill to install; repeat to select several.")
    install.add_argument("--overwrite", action="store_true", help="Replace a differing copy after preserving a backup.")
    export = commands.add_parser("export", help="Create a ZIP for manual import into another compatible client.")
    export.add_argument("--output", required=True)
    export.add_argument("--skill", action="append", default=[], help="Skill to export; repeat to select several.")
    return parser


def main() -> int:
    args = make_parser().parse_args()
    try:
        if args.command == "list":
            return run_list(args)
        if args.command == "install":
            return run_install(args)
        return run_export(args)
    except (FileExistsError, OSError, ValueError) as error:
        print("Error: " + str(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

