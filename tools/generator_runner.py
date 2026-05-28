import shutil
import subprocess
from pathlib import Path
from typing import Any

from tools.json_loader import save_json


class GeneratorRunner:
    def __init__(
        self,
        runtime_dir: Path,
        attack_config_relative_path: str,
        output_dataset_path: Path,
        run_command: list[str],
        suggested_config_path: str,
    ) -> None:
        self.runtime_dir = Path(runtime_dir)
        self.attack_config_path = self.runtime_dir / attack_config_relative_path
        self.output_dataset_path = Path(output_dataset_path)
        self.run_command = run_command
        self.suggested_config_path = Path(suggested_config_path)

    def generate_dataset(
        self,
        attack_config: dict[str, Any],
        iteration: int,
    ) -> str:
        self.runtime_dir.mkdir(parents=True, exist_ok=True)
        self.attack_config_path.parent.mkdir(parents=True, exist_ok=True)
        self.output_dataset_path.parent.mkdir(parents=True, exist_ok=True)
        self.suggested_config_path.parent.mkdir(parents=True, exist_ok=True)

        save_json(str(self.suggested_config_path), attack_config)
        save_json(str(self.attack_config_path), attack_config)

        result = subprocess.run(
            self.run_command,
            cwd=str(self.runtime_dir),
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode != 0:
            raise RuntimeError(
                "Synthetic generator execution failed.\n"
                f"Command: {' '.join(self.run_command)}\n"
                f"STDOUT:\n{result.stdout}\n"
                f"STDERR:\n{result.stderr}"
            )

        if not self.output_dataset_path.exists():
            raise FileNotFoundError(
                f"Expected generated dataset was not found: {self.output_dataset_path}"
            )

        iteration_dataset_path = (
            self.suggested_config_path.parent
            / f"dataset_iteration_{iteration}.csv"
        )

        shutil.copyfile(self.output_dataset_path, iteration_dataset_path)

        return str(iteration_dataset_path)
