from widgetastic.log import call_sig
from widgetastic.xpath import quote
from widgetastic.widget import ClickableMixin, Widget


class Button(Widget, ClickableMixin):
    """A Bootstrap button

    You can match by text, partial text or by attributes, you can also add the bootstrap classes
    into the matching.

    .. code-block:: python
        Button('Text of button (unless it is an input ...)')
        Button('contains', 'Text of button (unless it is an input ...)')
        Button(title='Show xyz')  # And such
        Button('Add', classes=[Button.PRIMARY])
        assert button.active
        assert not button.disabled

    """
    CHECK_VISIBILITY = True

    # Classes usable in the constructor
    # Button types
    DEFAULT = "btn-default"
    PRIMARY = "btn-primary"
    SUCCESS = "btn-success"
    INFO = "btn-info"
    WARNING = "btn-warning"
    DANGER = "btn-danger"
    LINK = "btn-link"

    # Button sizes
    LARGE = "btn-lg"
    MEDIUM = "btn-md"
    SMALL = "btn-sm"
    EXTRA_SMALL = "btn-xs"

    # Shape
    BLOCK = "btn-block"

    def __init__(self, parent, *text, **kwargs):
        logger = kwargs.pop("logger", None)
        Widget.__init__(self, parent, logger=logger)
        self.args = text
        self.kwargs = kwargs
        classes = kwargs.pop("classes", [])
        if text:
            if kwargs:  # classes should have been the only kwarg combined with text args
                raise TypeError("If you pass button text then only pass classes in addition")
            if len(text) == 1:
                self.locator_conditions = "normalize-space(.)={}".format(quote(text[0]))
            elif len(text) == 2 and text[0].lower() == "contains":
                self.locator_conditions = "contains(normalize-space(.), {})".format(quote(text[1]))
            else:
                raise TypeError("An illegal combination of text params")
        else:
            # Join the kwargs, if any
            self.locator_conditions = " and ".join(
                "@{}={}".format(attr, quote(value)) for attr, value in kwargs.items())

        if classes:
            if self.locator_conditions:
                self.locator_conditions += " and "
            self.locator_conditions += " and ".join(
                "contains(@class, {})".format(quote(klass))
                for klass in classes)
        if self.locator_conditions:
            self.locator_conditions = "and ({})".format(self.locator_conditions)

    def __locator__(self):
        return (
            './/*[(self::a or self::button or (self::input and (@type="button" or @type="submit")))'
            ' and contains(@class, "btn") {}]'.format(self.locator_conditions))

    @property
    def active(self):
        return "active" in self.browser.classes(self)

    @property
    def disabled(self):
        return ("disabled" in self.browser.classes(self) or
                self.browser.get_attribute("disabled", self) == "disabled" or
                self.browser.get_attribute("disabled", self) == "true")

    def __repr__(self):
        return "{}{}".format(type(self).__name__, call_sig(self.args, self.kwargs))

    @property
    def title(self):
        return self.browser.get_attribute("title", self)
