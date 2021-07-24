from typing import Callable


class EscapeHandler:
    ESCAPE_MAP = {  # TODO: Figure minimal
        "italic": "*",
        "bold": "*",
        "both": "*",
        "strikethrough": "~",
        "underline": "_",
    }

    def __getattr__(self, attr: str) -> Callable[[str], str]:
        return lambda string: string.replace(
            "\\" + self.ESCAPE_MAP[attr[7:]], self.ESCAPE_MAP[attr[7:]]
        )

    def __getitem__(self, item: str) -> Callable[[str], str]:
        return getattr(self, f"handle_{item}")

    @staticmethod
    def handle_normal(string: str) -> str:
        return string

    # @staticmethod
    # def handle_spec(string: str):
    #     return string.replace("\\:", ":")
    #
    # @staticmethod
    # def handle_italic(string: str):
    #     return string.replace("\\*", "*")


handle = EscapeHandler()
