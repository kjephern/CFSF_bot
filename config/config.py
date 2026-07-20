import tomllib
import typing

from box import Box
from pathlib import Path

FILE_ROOT = Path(__file__).parent.parent


def get_config(name: typing.Literal["general", "translator"]) -> Box:
    config_path = FILE_ROOT / "config" / f"{name}.toml"

    if not config_path.is_file():
        raise FileNotFoundError(f"設定檔未找到，預期路徑為: {config_path.resolve()}")

    with open(config_path, "rb") as f:
        return Box(tomllib.load(f), box_dots=True)
