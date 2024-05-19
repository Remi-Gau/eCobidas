"""Generates a typical landing page in english for an app."""

from pathlib import Path

from ecobidas.template_manager import TemplateManager


def main(output_dir: Path | None = None) -> None:
    if output_dir is None:
        output_dir = Path() / "output"

    TemplateManager.initialize()

    template = TemplateManager.env.get_template("landing_page.j2")

    rendered_template = template.render()
    with open(output_dir / "landing_page.html", "w") as out:
        out.write(f"{rendered_template}")


if __name__ == "__main__":
    main()
