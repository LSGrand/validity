import re

from typing import TYPE_CHECKING

from netmiko import BaseConnection, ConnectHandler

from .base import ConsecutivePoller


if TYPE_CHECKING:
    from validity.models import Command


class NetmikoPoller(ConsecutivePoller):
    host_param_name = "host"
    driver_disconnect_method = "disconnect"
    driver_factory = ConnectHandler

    def poll_one_command(self, driver: BaseConnection, command: "Command") -> str:
        custom_expect = rf"{re.escape(driver.base_prompt)}.*#"
        return driver.send_command(command.parameters["cli_command"],expect_string=custom_expect,read_timeout=60,delay_factor=2)
