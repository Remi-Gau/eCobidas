from jinja2 import Environment, FileSystemLoader, select_autoescape

from ecobidas.utils import root_dir


class TemplateManager:
    # Environment from which all templates will be loaded.
    # Required for Jinja imports
    env: Environment = None

    @classmethod
    def initialize(cls):
        """Initialize class variables.

        :return: None
        """
        # Set the class environment so that it relies on the right folder
        # and also auto-escapes our custom tmp files
        cls.env = Environment(
            loader=FileSystemLoader(root_dir() / "templates"),
            autoescape=select_autoescape(["html", "xml", "j2", "md"]),
        )

    @classmethod
    def render_template(cls, template_name: str, **kwargs) -> str:
        """Render the template after the provided name.

        :param template_name: Filename of the required template,
                              sans the .j2 extension.
        :param kwargs: Data used for the template rendering.

        :return: Rendered text for the requested template.
                 Includes any subtemplates in the hierarchy.
        """
        template_filename: str = f"{template_name}.j2"
        template = cls.env.get_template(template_filename)
        return template.render(kwargs["input_data"])
