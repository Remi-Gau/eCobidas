from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired, MultipleFileField
from markupsafe import Markup
from wtforms import (
    DateField,
    DecimalField,
    HiddenField,
    IntegerField,
    RadioField,
    SelectField,
    SelectMultipleField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import DataRequired, NumberRange


class UploadParticipantsForm(FlaskForm):
    participants = MultipleFileField(
        "Upload participants.tsv and participants.json",
        validators=[
            FileRequired(),
            FileAllowed(["tsv", "json"], "File must be '.tsv' and '.json' files."),
        ],
    )
    submit = SubmitField("Upload")


class UploadBoldJsonForm(FlaskForm):
    bold_json = FileField(
        "Upload bold.json",
        validators=[FileRequired(), FileAllowed(["json"], "The file must be a '.json' file.")],
    )
    submit_bold_json = SubmitField("Upload")


def generate_form(items=None, prefix=None, obj=None) -> FlaskForm:

    class DyanmicForm(FlaskForm):
        pass

    form = DyanmicForm

    for item_name, item in items.items():

        render_kw = (
            {"style": "border-color: green; border-width: 2px;"}
            if item["is_answered"]
            else {"style": "border-color: red; border-width: 2px;"}
        )

        validators = []
        if item["required"]:
            validators.append(DataRequired())

        question = f"{item['question']} {item['unit']}"

        if not item["visibility"]:
            setattr(
                form,
                item_name,
                HiddenField(
                    Markup(question),
                    validators=validators,
                    description=item["description"],
                    _prefix=prefix,
                ),
            )
            continue

        input_type = item["input_type"]

        default = None

        if input_type == "date":
            FieldType = DateField
            setattr(
                form,
                item_name,
                FieldType(
                    Markup(question),
                    validators=validators,
                    description=item["description"],
                    default=default,
                    _prefix=prefix,
                    format="%Y-%m-%d",
                    render_kw=render_kw,
                ),
            )

        elif input_type not in ["select", "radio", "slider"]:

            FieldType = StringField
            if input_type == "number":
                FieldType = IntegerField
            elif input_type == "float":
                FieldType = DecimalField
            elif input_type == "textarea":
                FieldType = TextAreaField

            if input_type in ["number", "float"]:
                minimum = item["min"]
                maximum = item["max"]
                validators.append(NumberRange(min=minimum, max=maximum))
                if minimum is not None and maximum is not None:
                    question += f" ({minimum=}, {maximum=})"
                elif minimum is not None:
                    question += f" ({minimum=})"

            setattr(
                form,
                item_name,
                FieldType(
                    Markup(question),
                    validators=validators,
                    description=item["description"],
                    default=default,
                    _prefix=prefix,
                    render_kw=render_kw,
                ),
            )

        elif input_type == "slider":

            min_label = float(item["choices"][0][1])
            max_label = float(item["choices"][-1][1])

            question += f" (min={min_label}, max={max_label})"

            FieldType = DecimalField
            validators.append(NumberRange(min=min_label, max=max_label))

            setattr(
                form,
                item_name,
                FieldType(
                    Markup(question),
                    validators=validators,
                    description=item["description"],
                    _prefix=prefix,
                    render_kw=render_kw,
                ),
            )

        else:

            form = add_choice_based_items(form, prefix, item_name, item)

    setattr(form, "submit", SubmitField("Save"))  # noqa B010

    return form(obj=obj)


def add_choice_based_items(form: FlaskForm, prefix: str, item_name: str, item: dict) -> FlaskForm:

    question = f"{item['question']} {item['unit']}"

    input_type = item["input_type"]

    render_kw = (
        {"style": "border-color: green; border-width: 2px;"}
        if item["is_answered"]
        else {"style": "border-color: red; border-width: 2px;"}
    )

    validators = []
    if item["required"]:
        validators.append(DataRequired())

    is_multiple = item["is_multiple"]

    if is_multiple:
        FieldType = SelectMultipleField
    elif input_type == "select":
        FieldType = SelectField
    elif input_type == "radio":
        FieldType = RadioField

    setattr(
        form,
        item_name,
        FieldType(
            Markup(question),
            validators=validators,
            description=item["description"],
            choices=item["choices"],
            _prefix=prefix,
            render_kw=render_kw,
        ),
    )

    return form
