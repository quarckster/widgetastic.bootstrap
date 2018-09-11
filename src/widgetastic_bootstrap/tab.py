from widgetastic.utils import ParametrizedLocator
from widgetastic.widget import View


class Tab(View):
    """Represents the Tab widget.

    Selects itself automatically when any child widget gets accessed, ensuring that the widget is
    visible.

    You can specify your own ``ROOT`` attribute on the class.
    """
    #: The text on the tab. If it is the same as the tab class name capitalized, can be omitted
    TAB_NAME = None

    #: Locator of the Tab selector
    TAB_LOCATOR = ParametrizedLocator(
        './/ul[contains(@class, "nav-tabs")]/li[./a[normalize-space(.)={@tab_name|quote}]]')

    @property
    def tab_name(self):
        return self.TAB_NAME or type(self).__name__.capitalize()

    def is_active(self):
        return 'active' in self.parent_browser.classes(self.TAB_LOCATOR)

    def is_disabled(self):
        return 'disabled' in self.parent_browser.classes(self.TAB_LOCATOR)

    @property
    def is_displayed(self):
        return self.parent_browser.is_displayed(self.TAB_LOCATOR)

    def click(self):
        return self.parent_browser.click(self.TAB_LOCATOR)

    def select(self):
        if not self.is_active():
            if self.is_disabled():
                raise ValueError(
                    'The tab {} you are trying to select is disabled'.format(self.tab_name))
            self.logger.info('opened the tab %s', self.tab_name)
            self.click()

    def child_widget_accessed(self, widget):
        # Select the tab
        self.select()

    def __repr__(self):
        return '<Tab {!r}>'.format(self.tab_name)
