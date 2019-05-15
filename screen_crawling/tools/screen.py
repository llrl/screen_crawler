import time
import uuid

from selenium import webdriver
from contextlib import contextmanager

from .data_loader import load_data


def init_driver():
    DRIVER = "chromedriver"
    driver = webdriver.Chrome(DRIVER)
    driver.fullscreen_window()
    return driver


def is_success(script_result):
    if not script_result:
        return True
    print(script_result)
    return script_result["success"] == 0


class ScreenCrawler:
    def __init__(self, driver, dirname, destroy_selectors=None, hide_selectors=None):
        self._driver = driver
        self._dirname = dirname
        self._destroy_selectors = destroy_selectors
        self._hide_selectors = hide_selectors

    def _execute_script_for_classes(self, html_selectors, raw_script):
        if self._destroy_selectors:
            for el_to_hide in html_selectors:
                for el in self._driver.find_elements_by_class_name(el_to_hide):
                    is_success(self._driver.execute_script(raw_script, el))

    def _destroy_trash(self):
        self._execute_script_for_classes(
            self._destroy_selectors, "arguments[0].style.display='none'"
        )

    def _hide_trash(self):
        self._execute_script_for_classes(
            self._hide_selectors, "arguments[0].style.visibility='hidden'"
        )

    def _mark_class_element(self, class_name, color):
        for el in self._driver.find_elements_by_class_name(class_name):
            is_success(
                self._driver.execute_script("arguments[0].style.background='red'", el)
            )

    def _screen(self, postfix_mark):
        self._driver.save_screenshot(
            f"{self._dirname}/{uuid.uuid4()}-{postfix_mark}.png"
        )

    @contextmanager
    def _save_example(self):
        filename = f"{self._dirname}/{uuid.uuid4()}"
        self._driver.save_screenshot(f"{filename}-raw.png")
        yield None
        self._driver.save_screenshot(f"{filename}-marked.png")

    def run(self, html_mark_selector, color="red"):
        self._destroy_trash()
        self._hide_trash()
        with self._save_example():
            self._mark_class_element(html_mark_selector, color)


def crawl(driver, page_data):
    driver.get(page_data.url)
    crawler = ScreenCrawler(
        driver, "dataset", page_data.destroy_classes, page_data.hide_classes
    )
    crawler.run(page_data.mark_class)


def run():
    driver = init_driver()
    try:
        data = load_data('tools/urls.data')
        for page_data in data:
            crawl(driver, page_data)
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
