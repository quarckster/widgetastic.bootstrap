import pytest
from widgetastic.utils import ParametrizedLocator
from widgetastic.widget import Text, View
from widgetastic_bootstrap import Accordion, Dropdown


class AccordionView(View):
    ROOT = ParametrizedLocator(".//div[@id='accordionExample']/..")

    def __init__(self, parent, id, logger=None):
        super(AccordionView, self).__init__(parent, logger=logger)
        self.id = id

    @View.nested
    class first(Accordion):
        ACCORDION_NAME = "Collapsible Group Item #1"
        content = Text(".//div[@class='card-body']")

    @View.nested
    class second(Accordion):
        ACCORDION_NAME = "Collapsible Group Item #2"
        dropdown = Dropdown("Accordion Dropdown button")

    @View.nested
    class third(Accordion):
        pass


@pytest.fixture
def view(browser, request):
    return AccordionView(browser, "accordionExample")


@pytest.mark.parametrize("accordion_name", ["first", "second", "third"])
def test_accordion_is_displayed(view, accordion_name):
    assert getattr(view, accordion_name).is_displayed


def test_child_widget_access(view):
    assert view.second.dropdown.is_displayed


def test_accordion_toggle(view):
    assert view.first.is_opened
    assert view.second.is_closed
    assert view.third.is_closed
    view.third.open()
    assert view.first.is_closed
    assert view.second.is_closed
    assert view.third.is_opened
    view.third.open()
    assert view.first.is_closed
    assert view.second.is_closed
    assert view.third.is_opened
    view.third.close()
    assert view.first.is_closed
    assert view.second.is_closed
    assert view.third.is_closed


def test_accordion_read(view):
    assert view.first.read() == {"content": "First accordion content"}


def test_accordion_name(view):
    assert view.first.accordion_name == "Collapsible Group Item #1"
    assert view.second.accordion_name == "Collapsible Group Item #2"
    assert view.third.accordion_name == "Third"
