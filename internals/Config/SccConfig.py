from __future__ import annotations

from typing import Literal


class SccConfig:
    """
    A configuration class for the scc command line tool.
    """

    exclude_dir: list[str] = []
    exclude_ext: list[str] = []
    include_ext: list[str] = []

    def __init__(self, config: dict[Literal["exclude-dir", "exclude-ext", "include-ext"], list[str]], parent_scc: SccConfig = None):
        """
        SccConfig constructor.
        :param config: The scc configuration from config file.
        :param parent_scc: If provided, the values of the parent will be used and extended by the repository-specific config.
        """
        # set parent config
        if parent_scc is not None:
            self.exclude_dir = parent_scc.exclude_dir
            self.exclude_ext = parent_scc.exclude_ext
            self.include_ext = parent_scc.include_ext
        # extend parent config with repository-specific config
        self.exclude_dir += [] if "exclude-dir" not in config else config["exclude-dir"]
        self.exclude_ext += [] if "exclude-ext" not in config else config["exclude-ext"]
        self.include_ext += [] if "include-ext" not in config else config["include-ext"]

    @property
    def subrepo_scc_config(self) -> SccConfig:
        """
        :return: The configuration for a sub repository.
                 Is the same as this one, but without the exclude-dir property.
        """
        return SccConfig({"include-ext": self.include_ext, "exclude-ext": self.exclude_ext})

    @property
    def scc_command_flags(self) -> list[str]:
        """
        :return: The flags for the scc command.
        """
        properties = ["--format", "json"]
        if self.exclude_dir:
            properties.append("--exclude-dir")
            properties.append(",".join(self.exclude_dir))
        if self.exclude_ext:
            properties.append("--exclude-ext")
            properties.append(",".join(self.exclude_ext))
        if self.include_ext:
            properties.append("--include-ext")
            properties.append(",".join(self.include_ext))
        return properties
