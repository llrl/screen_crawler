""" Module for make dataset using selenium.
ScreenCrawler generate raw and marked images and store in dataset folder.
"""
import uuid

from contextlib import contextmanager
from selenium import webdriver
from selenium.webdriver.common.by import By

from .data_loader import load_data


def init_driver():
    """ Init and return selenium driver with fullscreen window. """
    driver = webdriver.Chrome("chromedriver")
    driver.fullscreen_window()
    return driver


def is_success(script_result):
    """ Check screep result from driver.execute_script """
    if not script_result:
        return True
    print(script_result)
    return script_result["success"] == 0


class ScreenCrawler:
    """ Make screenshots and mark by selector. """

    def __init__(self, driver, dirname, destroy_selectors=None, hide_selectors=None):
        self._driver = driver
        self._dirname = dirname
        self._destroy_selectors = destroy_selectors
        self._hide_selectors = hide_selectors

    def _execute_script_for_classes(self, html_selectors, raw_script):
        if self._destroy_selectors:
            for html_selector in html_selectors:
                for found_element in self._driver.find_elements_by_class_name(html_selector):
                    is_success(self._driver.execute_script(raw_script, found_element))

    def _destroy_trash(self):
        self._execute_script_for_classes(
            self._destroy_selectors, "arguments[0].style.display='none'"
        )

    def _hide_trash(self):
        self._execute_script_for_classes(
            self._hide_selectors, "arguments[0].style.visibility='hidden'"
        )

    def _mark_class_element(self, class_name, color):
        for found_element in self._driver.find_elements_by_class_name(class_name):
            is_success(
                self._driver.execute_script(
                    f"arguments[0].style.background='{color}'", found_element
                )
            )

    def screen(self, postfix_mark):
        """ Maker screen and save to `_dirname` current position window of page. """
        self._driver.save_screenshot(
            f"{self._dirname}/{uuid.uuid4()}-{postfix_mark}.png"
        )

    @contextmanager
    def _save_example(self):
        filename = f"{uuid.uuid4()}"
        with open(f'{self._dirname}/info.txt', 'a') as f:
            f.write(f'{filename}.png\n')
        self._driver.save_screenshot(f"{self._dirname}/raw/{filename}.png")
        yield None
        self._driver.save_screenshot(f"{self._dirname}/marked/{filename}.png")

    def _fix_size(self, el, w, h):
        self._driver.execute_script(
                    f"arguments[0].style.width='{w}'", el
                )
        self._driver.execute_script(
                    f"arguments[0].style.height='{h}'", el
                )

    def _clear_example_element(self, el, classes_to_hide):
        """ main-goods__picture """
        for el_to_hide in classes_to_hide:
            found_el = el.find_element_by_class_name(el_to_hide)
            if found_el is None:
                continue
            self._driver.execute_script(
                        "arguments[0].style.visibility='hidden'", found_el
                    )

    def _save_element_example(self, el, color):
        filename = f"{uuid.uuid4()}"
        with open(f'{self._dirname}/info.txt', 'a') as f:
            f.write(f'{filename}.png\n')
        self._fix_size(el, 320, 200)
        el.screenshot(f"{self._dirname}/raw/{filename}.png")
        self._driver.execute_script(
            f"arguments[0].style.background='green'", el
        )
        marker = el.find_element_by_class_name('main-goods__title')
        self._driver.execute_script(
                    f"arguments[0].style.background='{color}'", marker
                )
        self._driver.execute_script(
                    f"arguments[0].style.color='{color}'", marker
                )

        red_price = el.find_element_by_class_name('main-goods__price')
        self._driver.execute_script(
                    f"arguments[0].style.background='darkseagreen'", red_price
                )

        red_price_color = el.find_element_by_class_name('main-goods__price')
        self._driver.execute_script(
                    f"arguments[0].style.color='darkseagreen'", red_price_color
                )
    
        pic = el.find_element_by_tag_name('img')
        self._driver.execute_script(
                    f"arguments[0].style.opacity='0'", pic
                )
        
        pic_d = el.find_element_by_class_name('main-goods__picture')
        self._driver.execute_script(
                    f"arguments[0].style.background='blue'", pic_d
                )

        el.screenshot(f"{self._dirname}/marked/{filename}.png")


    def run(self, box_selector, html_mark_selector, color="red"):
        """ Start crawler page and mark elements by `html_mark_selector`"""
        self._destroy_trash()
        self._hide_trash()
        red_price = self._driver.find_element_by_class_name('main-goods__price_color_red')
        self._driver.execute_script(
            f"arguments[0].style.color='darkseagreen'", red_price
        )
        for found_element in self._driver.find_elements_by_class_name(box_selector):
            self._save_element_example(found_element, color)

def crawl(driver, page_data):
    """ Crawl using driver and page data. """
    driver.get(page_data.url)
    crawler = ScreenCrawler(
        driver, "dataset", page_data.destroy_classes, page_data.hide_classes
    )
    crawler.run('main-goods__cell', 'main-goods__title')


def run():
    """ Main method for running screen_maker module """
    driver = init_driver()
    try:
        data = load_data("screen_marker/urls.data")
        for page_data in data:
            crawl(driver, page_data)
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
