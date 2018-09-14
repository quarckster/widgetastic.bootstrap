from wait_for import wait_for
from widgetastic.utils import ParametrizedLocator
from widgetastic.widget import do_not_read_this_widget, View, ClickableMixin


class Accordion(View, ClickableMixin):
    """Bootstrap accordions.

    They are like views that contain widgets. If a widget is accessed in the accordion, the
    accordion makes sure that it is open.

    You need to set the ``ACCORDION_NAME`` to correspond with the text in the accordion.
    If the accordion title is just a capitalized version of the accordion class name, you do not
    need to set the ``ACCORDION_NAME``.

    If the accordion is in an exotic location, you also have to change the ``ROOT``.
    https://getbootstrap.com/docs/4.1/components/collapse/#accordion-example

    """
    ACCORDION_NAME = None
    ROOT = ParametrizedLocator(
        './/div[contains(@class, "accordion")]//div[@class="card" and '
        './/div[@class="card-header"]//button[normalize-space(.)={@accordion_name|quote}]]')
    HEADER_LOCATOR = ".//button"

    @property
    def accordion_name(self):
        return self.ACCORDION_NAME or type(self).__name__.capitalize()

    @property
    def is_opened(self):
        attr = self.browser.get_attribute("aria-expanded", self.HEADER_LOCATOR)
        return attr.lower().strip() == "true"

    @property
    def is_closed(self):
        return not self.is_opened

    def click(self):
        """Override Clickable's click."""
        self.browser.click(self.HEADER_LOCATOR)

    def open(self):
        if self.is_closed:
            self.logger.info("opening")
            self.click()
            wait_for(lambda: self.is_opened, delay=0.1, num_sec=3)

    def close(self):
        if self.is_opened:
            self.logger.info("closing")
            self.click()

    def child_widget_accessed(self, widget):
        # Open the Accordion
        self.open()

    def read(self):
        if self.is_closed:
            do_not_read_this_widget()
        return super(Accordion, self).read()

    def __repr__(self):
        return '<Accordion {!r}>'.format(self.accordion_name)
