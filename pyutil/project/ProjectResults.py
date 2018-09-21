from pathlib import Path
from typing import *

from pyutil import IOUtils


class ProjectResults:

    def __init__(self):
        self.full_name: str = "UNKNOWN"
        self.results_dir: Path = None
        return

    @classmethod
    def get_project_results(cls, full_name: str, results_dir: Path = None, base_dir: Path = Path.cwd()/"_results") -> "ProjectResults":
        results = cls()
        results.full_name = full_name
        if results_dir is not None:
            results.results_dir = results_dir
        else:
            results.results_dir = base_dir / full_name
        # end if
        return results

    @property
    def meta_dir(self) -> Path:
        meta_dir: Path = self.results_dir / "META"
        meta_dir.mkdir(parents=True, exist_ok=True)
        return meta_dir

    def load_meta_result(self, file_name: str, fmt: str = "json") -> Any:
        return IOUtils.load(self.meta_dir / file_name, fmt)

    def dump_meta_result(self, file_name: str, data: Any, fmt: str = "json") -> None:
        IOUtils.dump(self.meta_dir / file_name, data, fmt)
        return

    def get_revision_dir(self, revision: str) -> Path:
        revision_dir = self.results_dir / revision
        revision_dir.mkdir(parents=True, exist_ok=True)
        return revision_dir

    def load_revision_result(self, revision: str, file_name: str, fmt: str = "json") -> Any:
        return IOUtils.load(self.get_revision_dir(revision) / file_name, fmt)

    def dump_revision_result(self, revision: str, file_name: str, data: Any, fmt: str = "json") -> None:
        IOUtils.dump(self.get_revision_dir(revision) / file_name, data, fmt)
        return
