import pytest
from widgetastic.widget import View
from widgetastic_bootstrap import Carousel


captions = {1: "First slide caption", 2: "Second slide caption", 3: "Third slide caption"}


@pytest.fixture
def view(browser):
    class TestView(View):
        carousel = Carousel(".//div[@id='carouselExampleIndicators']")

    return TestView(browser)


def test_carousel_slides_forward(view):
    for _, caption in captions.items():
        assert view.carousel.active_slide_caption == caption
        view.carousel.next_slide()


def test_carousel_slides_backward(view):
    for _, caption in reversed(list(captions.items())):
        view.carousel.previous_slide()
        assert view.carousel.active_slide_caption == caption


def test_carousel_slides_count(view):
    assert view.carousel.slides_count == 3


def test_carousel_slides_by_index(view):
    view.carousel.go_to_slide(3)
    assert view.carousel.active_slide_caption == "Third slide caption"
    view.carousel.go_to_slide(2)
    assert view.carousel.active_slide_caption == "Second slide caption"
