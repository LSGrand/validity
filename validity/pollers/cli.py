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

    def connect(self, credentials):
        driver = super().connect(credentials)
        if credentials.get("device_type") == "hp_comware":
            output = driver.send_command_timing('_cmdline-mode on', strip_prompt=False, strip_command=False)
            if 'continue' in output or 'Y/N' in output:
                output = driver.send_command_timing('y', strip_prompt=False, strip_command=False)
            if 'ssword' in output:
                driver.send_command_timing('512900', strip_prompt=False, strip_command=False)
            driver.set_base_prompt()
        return driver

    def poll_one_command(self, driver: BaseConnection, command: "Command") -> str:
        custom_expect = rf"{re.escape(driver.base_prompt)}.*[#>\]]"
        return driver.send_command(
            command.parameters["cli_command"],
            expect_string=custom_expect,
            read_timeout=90,
            delay_factor=2
        )
