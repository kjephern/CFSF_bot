import logging

from pathlib import Path

logger = logging.getLogger(__name__)

__all__ = ["get_cog_list"]


def get_cog_list() -> dict:
    """
    Returns:
        dict: {name: path}
    """
    FILE_ROOT = Path(__file__).parent.parent.parent
    base_dirs = ["cogs"]
    modules = {}

    for base in base_dirs:
        dir_path = FILE_ROOT / base

        if not dir_path.is_dir():
            logger.warning(f"資料夾不存在: {dir_path}，已跳過。")
            continue

        for path in dir_path.iterdir():
            is_py_file = path.is_file() and path.suffix == ".py" and path.name != "__init__.py"

            is_cog_package = path.is_dir() and (path / "__init__.py").exists()

            if is_py_file:
                module_name = path.stem
                module_path = f"Bot.{base}.{module_name}"
                modules[module_name] = module_path

            elif is_cog_package:
                module_name = path.name
                module_path = f"Bot.{base}.{module_name}"
                modules[module_name] = module_path

            elif path.is_dir():
                for sub_path in path.iterdir():
                    is_sub_py = sub_path.is_file() and sub_path.suffix == ".py" and sub_path.name != "__init__.py"
                    is_sub_pkg = sub_path.is_dir() and (sub_path / "__init__.py").exists()

                    if is_sub_py or is_sub_pkg:
                        sub_name = sub_path.stem if is_sub_py else sub_path.name
                        module_path = f"Bot.{base}.{path.name}.{sub_name}"
                        modules[sub_name] = module_path

    return modules
