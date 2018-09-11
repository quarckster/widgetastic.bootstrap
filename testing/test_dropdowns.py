import pytest
from widgetastic.widget import View
from widgetastic_bootstrap import (Dropdown, DropdownDisabled, DropdownItemDisabled,
                                   DropdownItemNotFound)


@pytest.fixture
def view(browser):
    class TestView(View):
        dropdown_button = Dropdown("Dropdown button")
        dropdown_link = Dropdown("Dropdown link")
        disabled_dropdown = Dropdown("Disabled dropdown button")

    return TestView(browser)


@pytest.fixture(params=["dropdown_button", "dropdown_link", "disabled_dropdown"])
def dropdown(view, request):
    return getattr(view, request.param)


def test_dropdown_is_displayed(dropdown):
    assert dropdown.is_displayed


def test_disabled_dropdown(dropdown):
    if dropdown.text == "Disabled dropdown button":
        assert not dropdown.is_enabled
    else:
        assert dropdown.is_enabled


def test_dropdown_items(dropdown):
    assert dropdown.items == ["Action", "Another action", "Something else here"]
    assert dropdown.has_item("Another action")
    assert not dropdown.has_item("Non existing items")
    if dropdown.text == "Disabled dropdown button":
        with pytest.raises(DropdownDisabled):
            dropdown.item_enabled("Action")
    else:
        assert dropdown.item_enabled("Action")
        assert not dropdown.item_enabled("Another action")


def test_dropdown_open(dropdown):
    assert not dropdown.is_open
    if dropdown.text == "Disabled dropdown button":
        with pytest.raises(DropdownDisabled):
            dropdown.open()
    else:
        dropdown.open()
        assert dropdown.is_open
        dropdown.close()
        assert not dropdown.is_open


def test_dropdown_item_select(dropdown):
    if dropdown.text == "Disabled dropdown button":
        with pytest.raises(DropdownDisabled):
            dropdown.item_select("Action")
    else:
        dropdown.item_select("Action")
        assert not dropdown.is_open
        with pytest.raises(DropdownItemDisabled):
            dropdown.item_select("Another action")
        with pytest.raises(DropdownItemNotFound):
            dropdown.item_select("Non existing items")
