from widgetastic.utils import ParametrizedLocator
from widgetastic.xpath import quote
from widgetastic.widget import View


class Tab(View):
    """Represents the Tab widget.

    Selects itself automatically when any child widget gets accessed, ensuring that the widget is
    visible.
    https://getbootstrap.com/docs/4.1/components/navs/#tabs

    You can specify your own ``ROOT`` attribute on the class.
    """
    #: The text on the tab. If it is the same as the tab class name capitalized, can be omitted
    TAB_NAME = None

    #: Locator of the Tab selector
    TAB_LOCATOR = ParametrizedLocator(
        './/ul[contains(@class, "nav-tabs") or contains(@class, "nav-pills")]'
        '/li/a[normalize-space(.)={@tab_name|quote}]')

    @property
    def tab_name(self):
        return self.TAB_NAME or type(self).__name__.capitalize()

    @property
    def is_active(self):
        return "active" in self.parent_browser.classes(self.TAB_LOCATOR)

    @property
    def is_disabled(self):
        return "disabled" in self.parent_browser.classes(self.TAB_LOCATOR)

    @property
    def is_displayed(self):
        return self.parent_browser.is_displayed(self.TAB_LOCATOR)

    def click(self):
        return self.parent_browser.click(self.TAB_LOCATOR)

    def select(self):
        if not self.is_active:
            if self.is_disabled:
                raise ValueError(
                    "The tab {} you are trying to select is disabled".format(self.tab_name))
            self.logger.info("opened the tab %s", self.tab_name)
            self.click()

    def child_widget_accessed(self, widget):
        # Select the tab
        self.select()

    def __repr__(self):
        return "<Tab {!r}>".format(self.tab_name)


class GenericTabWithDropdown(Tab):
    """Tab with a dropdown. Variant that always takes the sub item name in the select().

    Does not support automatic reveal of the tab upon access as the default dropdown item is not
    specified.
    """
    DROPDOWN = "./div/a[normalize-space(.)={}]"

    @property
    def _parent_classes(self):
        parent = self.parent_browser.element(self.TAB_LOCATOR)
        return self.parent_browser.classes("./parent::li", parent=parent)

    @property
    def is_dropdown(self):
        return "dropdown" in self._parent_classes

    @property
    def is_open(self):
        return "show" in self._parent_classes

    def open(self):
        if not self.is_open:
            self.logger.info("opened the tab %s", self.tab_name)
            self.click()

    def close(self):
        if self.is_open:
            self.logger.info("closed the tab %s", self.tab_name)
            self.click()

    def select(self, sub_item):
        if not self.is_dropdown:
            raise TypeError("{} is not a tab with dropdown and CHECK_IF_DROPDOWN is True")
        self.open()
        el = self.parent_browser.element(self.TAB_LOCATOR)
        parent = self.parent_browser.element("./parent::li", parent=el)
        self.logger.info("clicking the sub-item %r", sub_item)
        self.parent_browser.click(self.DROPDOWN.format(quote(sub_item)), parent=parent)

    def child_widget_accessed(self, widget):
        """Nothing. Since we don't know which sub_item."""

    def __repr__(self):
        return "<TabWithDropdown {!r}>".format(self.tab_name)


class TabWithDropdown(GenericTabWithDropdown):
    """Tab with the dropdown and its selection item set so child_widget_accessed work as usual."""
    #: Specify the dropdown item here
    SUB_ITEM = None

    def select(self):
        return super(TabWithDropdown, self).select(self.SUB_ITEM)

    def child_widget_accessed(self, widget):
        # Redefine it back like in Tab since TabWithDropdown removes it
        self.select()

    def __repr__(self):
        return "<TabWithDropdownDefault {!r}>".format(self.tab_name)
