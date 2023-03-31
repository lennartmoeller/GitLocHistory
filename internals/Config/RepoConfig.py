from __future__ import annotations

from internals.Config.SccConfig import SccConfig


class RepoConfig:
    """
    A configuration class for a git repository.
    """

    _url: str
    _dir: str
    _include_submodules: bool
    _scc: SccConfig

    def __init__(self, config: dict, parent_scc: SccConfig):
        """
        RepoConfig constructor.
        :param config: The repository configuration from config file.
        :param parent_scc: The global scc configuration.
                           Used unless overridden by the repository specific scc configuration.
        """
        # set url
        if "url" not in config:
            raise Exception("Repo URL is required")
        self._url = config["url"]
        # set dir
        self._dir = "." if "dir" not in config else config["dir"]
        # set include submodules
        self._include_submodules = True if "include_submodules" not in config else config["include_submodules"]
        # set scc config
        self._scc = SccConfig({} if "scc" not in config else config["scc"], parent_scc)

    @property
    def url(self) -> str:
        """
        :return: The url of the repository.
        """
        return self._url

    @property
    def dir(self) -> dir:
        """
        :return: The directory relative to the repository directory in which to count the number of lines.
        """
        return self._dir

    @property
    def include_submodules(self) -> bool:
        """
        :return: Whether to include submodules and their commit in the count.
        """
        return self._include_submodules

    @property
    def scc(self) -> SccConfig:
        """
        :return: The scc configuration for this repository.
        """
        return self._scc

    def get_subrepo_config(self, url: str):
        """
        :param url: The url of the sub repository.
        :return: The configuration for a sub repository.
        """
        config = RepoConfig({"url": url}, self._scc.subrepo_scc_config)
        return config
