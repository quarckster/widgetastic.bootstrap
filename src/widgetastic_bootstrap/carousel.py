from wait_for import wait_for
from widgetastic.utils import ParametrizedLocator
from widgetastic.xpath import quote
from widgetastic.widget import do_not_read_this_widget, Widget


class Carousel(Widget):
    """Represents the Carousel widget.

    https://getbootstrap.com/docs/4.1/components/carousel/

    """
    ROOT = ParametrizedLocator("{@locator}")
    SLIDE_CONTROL = "./a[@data-slide={}]"
    INDICATOR = "./ol/li[@data-slide-to={}]"
    CAPTION = ".//div[contains(@class, 'active')]/div[contains(@class, 'carousel-caption')]"
    SLIDES = ".//div[contains(@class, 'carousel-item')]"

    def __init__(self, parent, locator, logger=None):
        super(Carousel, self).__init__(parent, logger=logger)
        self.locator = locator

    def _change_slide_to(self, direction=None, index=None):
        if direction:
            el = self.browser.element(self.SLIDE_CONTROL.format(quote(direction)))
        if index:
            el = self.browser.element(self.INDICATOR.format(index - 1))
        self.browser.click(el)
        active_slide = self._active_slide
        wait_for(lambda: "active" not in self.browser.classes(active_slide), delay=0.1, num_sec=3)

    @property
    def _active_slide(self):
        for el in self.browser.elements(self.SLIDES, parent=self):
            if "active" in self.browser.classes(el):
                return el

    def previous_slide(self):
        self._change_slide_to(direction="prev")

    def next_slide(self):
        self._change_slide_to(direction="next")

    def go_to_slide(self, index):
        self._change_slide_to(index=index)

    @property
    def active_slide_caption(self):
        return self.browser.text(self.CAPTION, parent=self)

    @property
    def slides_count(self):
        return len(self.browser.elements(self.SLIDES, parent=self))

    def read(self):
        do_not_read_this_widget()
