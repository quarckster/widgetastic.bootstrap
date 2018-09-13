import pytest
from widgetastic.utils import ParametrizedLocator
from widgetastic.widget import Text, View
from widgetastic_bootstrap import Tab, TabWithDropdown


class TabsView(View):
    ROOT = ParametrizedLocator(".//ul[@id={@id|quote}]/..")
    tabs_names = ["home", "profile", "disabled", "dropdown"]

    def __init__(self, parent, id, logger=None):
        super(TabsView, self).__init__(parent, logger=logger)
        self.id = id

    @View.nested
    class home(Tab):
        pass

    @View.nested
    class profile(Tab):
        PROFILE = ParametrizedLocator("//div[@id=concat({@parent/id|quote}, '-profile')]")
        content = Text(PROFILE)

    @View.nested
    class disabled(Tab):
        pass

    @View.nested
    class dropdown(TabWithDropdown):
        SUB_ITEM = "Action"
        pass


@pytest.fixture(params=["tabs", "pills"])
def view(browser, request):
    return TabsView(browser, request.param)


@pytest.mark.parametrize("tab_name", TabsView.tabs_names)
def test_tabs_is_displayed(view, tab_name):
    assert getattr(view, tab_name).is_displayed


def test_child_widget_accessed(view):
    assert view.profile.content.text == "Profile text"


def test_tab_active(view):
    assert view.home.is_active


def test_tab_disabled(view):
    assert view.disabled.is_disabled


def test_tab_dropdown(view):
    assert view.dropdown.is_dropdown


def test_tab_dropdown_toggle(view):
    assert not view.dropdown.is_open
    view.dropdown.open()
    assert view.dropdown.is_open
    view.dropdown.close()
    assert not view.dropdown.is_open


def test_tab_dropdown_select(view):
    view.dropdown.select()
