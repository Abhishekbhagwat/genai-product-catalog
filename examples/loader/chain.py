# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Dict, List, Any
from abc import ABC, abstractmethod


class Context:
    def __init__(self):
        self.values: Dict[str, Any] = {}

    def has_key(self, key: str) -> bool:
        """
        A helper method to determine if a key is present
        :param key: string value of the key
        :return: boolean value if present and Not None
        """
        return self.values[key] is not None

    def add_value(self, key: str, value: Any) -> None:
        """
        A helper method for adding values to the backing dictionary.
        :param key:  string value of the key
        :param value: any type of object
        """
        self.values[key] = value

    def get_value(self, key: str) -> Any:
        """
        A helper method for getting values
        :param key: the string value of the key to return
        :return: any object or None if not present
        """
        return self.values[key] if self.has_key(key) else None


class Command(ABC):
    """
    A command is an abstract definition for class that MAY execute against
    a given context.
    """
    @abstractmethod
    def is_executable(self, context: Context) -> bool:
        """
          Determines if the command SHOULD be executed based on values in the
          context.
        """
        return False

    @abstractmethod
    def execute(self, context: Context) -> None:
        """If executable, run the command, otherwise return"""
        pass


class Chain(Command, ABC):
    """
    A chain is a collection of commands that execute for given workflows.
    Since a chain is also a command, complex workflows can be created
    by having chains be composed of multiple chains.

    Note: chain DOES NOT implement is_executable or execute from the parent
    class.
    """
    def __init__(self):
        self.commands: List[Command] = []

    def add_command(self, command: Command) -> None:
        """
        Adds a command to the internal state.
        :param command: A command to execute
        :return: None
        """
        self.commands.append(command)


class BaseChain(Chain):
    def __init__(self):
        super()

    def is_executable(self, context: Context) -> bool:
        return len(self.commands) > 0

    def execute(self, ctx: Context) -> None:
        for cmd in self.commands:
            if cmd.is_executable(ctx):
                cmd.execute(ctx)
