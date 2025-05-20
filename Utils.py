import os


class Utils:
    @staticmethod
    def sync_print(message: str) -> None:
        """Synchronous echo

        Args:
            message (str): message to display in echo
        """
        os.system(f"echo '{message}'")
    
    @staticmethod
    def h1(message: str, type: str = "INFO") -> None:
        """Returns pretty message

        Args:
            message (str): message to display in console
            type (str, optional): message type. Defaults to 'INFO'.
        """
        Utils.sync_print(
            f"[{type}] ------------------------------------------------------------------------"
        )
        Utils.sync_print(f"[{type}] {message}")
        Utils.sync_print(
            f"[{type}] ------------------------------------------------------------------------"
        )