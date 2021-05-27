from typing import Any, Dict
from urllib.parse import quote, urlencode
from uuid import uuid4

from lime_python import Command, CommandMethod


class ExtensionBase:
    """Class base to all sdk extensions."""

    def __init__(self, client: Any, to: str = None) -> None:
        self.client = client
        self.to = to

    def create_get_command(
        self,
        uri: str,
        id: str = None
    ) -> Command:
        """Create a get Command.

        Args:
            uri (str): Command uri
            id (str): Comand id

        Returns:
            Command
        """
        command = Command(CommandMethod.GET, uri)
        id = id if id else str(uuid4())
        command.id = command

        if self.to:
            command.to = self.to

        return command

    def create_set_command(
        self,
        uri: str,
        resource: Any,
        type_n: str = None,
        id: str = None
    ) -> Command:
        """Create a set Command.

        Args:
            uri (str): Command uri
            type_n (str): resource mime type
            resource (Any): Command resource
            id (str): Command id

        Returns:
            Command
        """
        command = Command(CommandMethod.SET, uri, type_n, resource)
        id = id if id else str(uuid4())
        command.id = command

        if self.to:
            command.to = self.to

        return command

    def create_merge_command(
        self,
        uri: str,
        resource: Any,
        type_n: str = None,
        id: str = None
    ) -> Command:
        """Create a merge Command.

        Args:
            uri (str): Command uri
            type_n (str): resource mime type
            resource (Any): Command resource
            id (str): Command id

        Returns:
            Command
        """
        command = Command(CommandMethod.MERGE, uri, type_n, resource)
        id = id if id else str(uuid4())
        command.id = command

        if self.to:
            command.to = self.to

        return command

    def create_delete_command(
        self,
        uri: str,
        id: str = None
    ) -> Command:
        """Create a delete Command.

        Args:
            uri (str): Command uri
            id (str): Command id

        Returns:
            Command
        """
        command = Command(CommandMethod.DELETE, uri)
        id = id if id else str(uuid4())
        command.id = command

        if self.to:
            command.to = self.to

        return command

    async def process_command_async(
        self,
        command: Command
    ) -> Command:
        """Process a command async.

        Args:
            command (Command): the Command to process

        Returns:
            Command: the response
        """
        command.id = command.id if command.id else str(uuid4())

        return await self.client.process_command_async(command)

    def build_resource_query(
        self,
        uri: str,
        query: Dict[str, str]
    ) -> str:
        """Build the resource query.

        Args:
            uri (str): base uri
            query (Dict[str, str]): items to add

        Returns:
            str: final uri
        """
        if not uri.endswith('?'):
            uri += '?'  # noqa: WPS336
        return f'{uri}{urlencode(query)}'

    def build_uri(self, uri: str, **kwargs: dict) -> str:
        """Build a uri with parameters.

        Args:
            uri (str): the template uri with {{params}}
            kwargs: the parameters to replace

        Returns:
            str: the final uri
        """
        for name, value in kwargs.items():
            placeholder = '{{' + name + '}}'  # noqa: WPS336
            uri = uri.replace(placeholder, quote(value))
        return uri
