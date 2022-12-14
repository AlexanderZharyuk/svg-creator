import argparse
import logging

from textwrap import dedent


logging_format = "[%(levelname)s] %(message)s"
logging.basicConfig(format=logging_format)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def get_xml_for_convert(figure: str, size: str, color: str) -> str:
    """
    Функция отдает XML-строку для дальнейшего сохранения его в SVG-формате.
    """

    svg_main_properties = dedent(
        """\
        <?xml version="1.0" encoding="UTF-8"?>
            <svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080">
                {figure_properties}
            </svg>
        """
    )
    circle_svg_properties = svg_main_properties.format(
        figure_properties=f"<circle r='{size}' cy='{size}' cx='{size}' "
                          f"fill='{color}'/>"
    )
    square_svg_properties = svg_main_properties.format(
        figure_properties=f"<rect width='{size}' height='{size}' "
                          f"fill='{color}'/>"
    )

    available_figures = {
        "circle": circle_svg_properties,
        "square": square_svg_properties
    }
    return available_figures[figure]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "figure", help="Выберите фигуру, доступны: circle и square", type=str
    )
    parser.add_argument(
        "size", help="Радиус окружности или длина стороны квадрата.", type=str
    )
    parser.add_argument(
        "color",
        help="Цвет фигуры.",
        type=str
    )
    parser.add_argument(
        "filepath",
        help="Путь и название файла.",
        type=str,
        nargs="?",
        default="./result.svg"
    )
    arguments = parser.parse_args()

    try:
        xml_string = get_xml_for_convert(
            arguments.figure,
            arguments.size,
            arguments.color
        )
    except KeyError:
        logger.error(
            "Такая фигура не поддерживается. Используйте circle или square."
        )
    else:
        with open(arguments.filepath, "w") as file:
            file.write(xml_string)
        logger.info("Файл сохранен!")


if __name__ == "__main__":
    main()
