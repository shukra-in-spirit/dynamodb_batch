from rich.text import Text

class rich_tui:
    def __init__(self) -> None:
        pass

    def create_print_string(strings_with_styles_list):
        text = Text()
        for string_with_style in strings_with_styles_list:
            string, style = string_with_style
            text.append(string, style)
        return text