from widgetastic.widget import View
from widgetastic_bootstrap import BreadCrumb


def test_breadcrumbs(browser):
    class TestView(View):
        breadcrumbs = BreadCrumb()

    view = TestView(browser)
    assert view.breadcrumbs.is_displayed
    assert view.breadcrumbs.active_location == view.breadcrumbs.read() == "Data"
    assert view.breadcrumbs.locations == ["Home", "Library", "Data"]
    assert view.breadcrumbs.click_location("Home") is None
