import re
import time
from typing import Any, Callable, Optional

from mcdreforged.api.all import *

from just_kill_it.config import Configuration

stop_sign: bool = False
server_saved: bool = False
config: Optional[Configuration] = None
psi: Optional[PluginServerInterface] = ServerInterface.psi()
metadata: Metadata = psi.get_self_metadata()


def tr(key: str, *args, **kwargs) -> RTextMCDRTranslation:
    return psi.rtr('{}.{}'.format(metadata.id, key), *args, **kwargs)


@new_thread(metadata.name)
def wait_and_kill(condition: Callable[[], bool], timeout: int) -> Any:
    if timeout < 0:
        return
    timeout *= 10
    while timeout > 0:
        if condition() or stop_sign:
            print('canceled')
            return
        time.sleep(0.1)
        timeout -= 1
    psi.logger.info(tr('killing'))
    return psi.kill()


def wait_for_save():
    wait_and_kill(lambda: server_saved, config.save_timeout)


def wait_for_exit():
    wait_and_kill(lambda: stop_sign, config.exit_timeout)


def on_info(_, info: Info):
    global server_saved
    if not info.is_user:
        if re.fullmatch(config.stopping_pattern, info.content):
            psi.logger.info(tr('stopping', config.save_timeout))
            wait_for_save()
        if re.fullmatch(config.saved_pattern, info.content):
            psi.logger.info(tr('saved', config.exit_timeout))
            server_saved = True
            wait_for_exit()


def on_load(_, old):
    global config
    config = Configuration.load()


def on_unload(_):
    global stop_sign
    stop_sign = True
