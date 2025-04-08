from typing import List

from mcdreforged.api.types import PluginServerInterface
from mcdreforged.api.utils import Serializable

import just_kill_it

class Configuration(Serializable):
    stopping_pattern: str = 'Stopping the server'
    save_timeout: int = 120
    saved_pattern: str = '.*All dimensions are saved'
    exit_timeout: int = 10

    @staticmethod
    def get_psi() -> PluginServerInterface:
        return just_kill_it.psi

    @classmethod
    def load(cls) -> 'Configuration':
        return cls.get_psi().load_config_simple(target_class=cls)

    def save(self):
        self.get_psi().save_config_simple(self)
