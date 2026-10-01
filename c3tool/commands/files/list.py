"""List one directory."""

from c3tool.commands.files._paths import expand_path
from c3tool.model import BaseCommand, CommandError, CommandSpec, ToolContext

COMMAND_SPEC = CommandSpec("ls", "<filepath, default current>", "Lists a directory.", "python3 script.py ls [filepath]", "Directory entries with type and size.", "c3tool.commands.files.list:ListCommand", order=8)


class ListCommand(BaseCommand):
    def run(self, args, context: ToolContext) -> str:
        self.require_range(args, 0, 1, COMMAND_SPEC.usage)

        target = expand_path(args[0], context) if args else context.cwd
        if not target.is_dir():
            raise CommandError(f"Directory not found: {target}")

        entries = sorted(target.iterdir(), key=lambda item: item.name.casefold())
        if not entries:
            return f"Directory is empty: {target}"

        rows = [f"{describe(item):<5} {size_of(item):>10}  {item.name}" for item in entries]
        return "\n".join([f"Directory: {target}", *rows])


def describe(path) -> str:
    if path.is_symlink():
        return "link"
    if path.is_dir():
        return "dir"
    if path.is_file():
        return "file"
    return "other"


def size_of(path) -> int:
    try:
        return path.lstat().st_size
    except OSError:
        return 0
