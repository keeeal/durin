from argparse import ArgumentParser
from collections.abc import Callable
from importlib import import_module
from itertools import count
from pathlib import Path
from typing import Any

from build123d import export_step, export_stl
from build123d.topology.shape_core import Shape
from ocp_vscode import save_screenshot, show
from yaml import safe_load

EXPORT_FUNCTIONS: dict[str, Callable[[Shape, Path], None]] = {
    "stl": export_stl,
    "step": export_step,
}


def load_config(path: Path) -> dict[str, dict[str, Any]]:
    with open(path) as file:
        return safe_load(file)


def import_class(class_path: str) -> Any:
    module_path, class_name = class_path.rsplit(".", 1)
    module = import_module(module_path)
    return getattr(module, class_name)


def build_part(
    config: dict[str, dict[str, Any]],
    part_name: str,
) -> Shape:
    if part_name not in config:
        msg = f"Unexpected part name: {part_name}"
        raise ValueError(msg)

    part_config = config[part_name]
    part_class = import_class(part_config["class"])
    part = part_class(**part_config["config"])
    assert isinstance(part, Shape)
    return part


def view(
    config_path: Path,
    part_name: str,
    screenshot: bool = False,
) -> None:
    config = load_config(config_path)
    part = build_part(config, part_name)
    show(part)
    if screenshot:
        output_dir = Path() / "screenshots"
        output_dir.mkdir(parents=True, exist_ok=True)
        for index in count():
            output_path = output_dir / f"{part_name}_{index:04d}.png"
            if not output_path.exists():
                break
        save_screenshot(output_path.as_posix())


def export(
    config_path: Path,
    part_name: str | None,
    format: str,
    output_dir: Path,
) -> None:
    format = format.lower()
    if format not in EXPORT_FUNCTIONS:
        msg = f"Unexpected format: {format}"
        raise ValueError(msg)

    config = load_config(config_path)
    part_names = (
        [part_name]
        if part_name
        else [
            part_name
            for part_name, part_config in config.items()
            if part_config.get("export")
        ]
    )
    for part_name in part_names:
        output_path = output_dir / f"{part_name}.{format}"
        export_function = EXPORT_FUNCTIONS[format]
        part = build_part(config, part_name)
        output_dir.mkdir(parents=True, exist_ok=True)
        export_function(part, output_path)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "--config-path",
        type=Path,
        default=Path() / "src" / "cad" / "config.yaml",
    )
    subparsers = parser.add_subparsers(required=True)

    parser_view = subparsers.add_parser("view", help="Visualize parts")
    parser_view.set_defaults(function=view)
    parser_view.add_argument("--part-name", default="main")
    parser_view.add_argument("--screenshot", action="store_true")

    parser_export = subparsers.add_parser("export", help="Export parts to file")
    parser_export.set_defaults(function=export)
    parser_export.add_argument("--part-name", default=None)
    parser_export.add_argument(
        "--format",
        type=str.lower,
        choices=EXPORT_FUNCTIONS,
        default="stl",
    )
    parser_export.add_argument("--output-dir", type=Path, default=Path() / "parts")
    args = vars(parser.parse_args())
    args.pop("function")(**args)
