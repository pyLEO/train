"""
this module solve login
"""


from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import time
from PIL import Image
from io import BytesIO
from apis.codes import get_qunar_id, get_qunar_result


# options = webdriver.ChromeOptions()
# user_agent = '--user-agent=Mozilla/5.0 (iPod; U; CPU iPhone OS 2_1 like ' \
#             'Mac OS X; ja-jp) AppleWebKit/525.18.1 (KHTML, like Gecko) ' \
#             'Version/3.1.1 Mobile/5F137 Safari/525.20'
# options.add_argument(user_agent)
# browser = webdriver.Chrome(chrome_options=options)


def user_login(username, password):
    """
    :param username:
    :param passwd:
    :return:
    """

    browser = webdriver.Chrome()
    browser.implicitly_wait(10)
    browser.get("https://kyfw.12306.cn/otn/login/init")
    time.sleep(2)
    WebDriverWait(browser, 10).until(lambda x: x.find_element_by_css_selector('img.touclick-image'))
    screen_shot = browser.get_screenshot_as_png()
    element = browser.find_element_by_css_selector('img.touclick-image')
    left = element.location['x']
    top = element.location['y']
    right = element.location['x'] + element.size['width']
    bottom = element.location['y'] + element.size['height']
    im = Image.open(BytesIO(screen_shot))
    im = im.crop((left, top, right, bottom))
    im.save(r'C:\b.png')
    result_list = get_qunar_result(get_qunar_id(r'C:\b.png'))

    action = ActionChains(browser)
    for i in range(0, len(result_list), 2):
        y_move = int(result_list[i+1]) + 30
        action.move_to_element_with_offset(element, result_list[i], y_move).click().perform()

    browser.find_element_by_css_selector("input#username").send_keys(username)
    browser.find_element_by_css_selector("input#password").send_keys(password)
    browser.find_element_by_css_selector("a#loginSub").click()
    return None


user_login('aleo100', '840727lh')