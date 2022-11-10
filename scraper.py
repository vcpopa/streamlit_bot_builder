class Bot():
    def __init__(self,param_dict):
        self.scraper_name=param_dict["scraper_name"]
        self.link_to_scrape=param_dict["link_to_scrape"]
        self.download_path=param_dict["download_path"]

    def bot_template(self):
        if self.download_path is not None:
            download_dir_options="""
chrome_options.add_experimental_option("download.default_directory","{}") """.format(self.download_path)
        else:
            download_dir_options="\n"


        self.template=f"""
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--profile-directory=Default')
chrome_options.add_argument('--user-data-dir=~/.config/google-chrome')
{download_dir_options}
driver=webdriver.Chrome("./chromedriver",options=chrome_options)
driver.implicitly_wait(10)
driver.get({self.link_to_scrape})
driver.maximize_window() 
"""

        return self.template

class Actions():
    def __init__(self,param_dict):
        self.template=""
        self.param_dict=param_dict
        self.action_type=param_dict['action']
        self.find_by=self.param_dict['find_by']
        self.dom_element=self.param_dict['dom_element']
        self.wait_for=self.param_dict['wait_for']
        self.keys_to_send=self.param_dict['keys_to_send']

    def generate_action_template(self):

        if self.action_type=="Click":
            self.template=self.template
            if self.param_dict['find_by']=="CSS SELECTOR":
                self.template=self.template +"\n"
                self.template=self.template+f"""
click_data=driver.find_element(By.CSS_SELECTOR,{self.dom_element})
click_data.click() 
                """
            if self.param_dict['find_by']=="XPATH":
                self.template=self.template +"\n"
                self.template=f"""
click_data=driver.find_element(By.XPATH,'{self.dom_element}')
click_data.click()
                """
            if self.wait_for is None:
                self.template=self.template
            else:
                self.template=self.template +"\n"
                self.template=self.template+f"\ntime.sleep({self.wait_for})"
###################################################################################################################
        elif self.action_type=="Write":
            if self.param_dict['find_by']=="CSS SELECTOR":
                self.template=self.template +"\n"
                self.template=f"""
write_data=driver.find_element(By.CSS_SELECTOR,{self.dom_element})
write_data.send_keys({self.keys_to_send})
            """
            if self.param_dict['find_by']=="XPATH":
                self.template=self.template +"\n"
                self.template=f"""
write_data=driver.find_element(By.XPATH,{self.dom_element})
write_data.send_keys({self.keys_to_send})
            """
            if self.wait_for is None:
                self.template=self.template
            else:
                self.template=self.template +"\n"
                self.template=self.template+(f"\ntime.sleep({self.wait_for})")
######################################################################################################################
        elif self.action_type=="Hit Enter":
            if self.wait_for is None:
                self.template=self.template

            else:
                self.template=self.template +"\n"
                self.template=self.template+(f"\ntime.sleep({self.wait_for})")

            if self.param_dict['find_by']=="CSS SELECTOR":
                self.template=self.template +"/n"
                self.template=f"""
write_data=driver.find_element(By.CSS_SELECTOR,{self.dom_element})
write_data.send_keys({"/n"}) 
                """
            if self.param_dict['find_by']=="XPATH":
                self.template=self.template +"\n"
                self.template=f"""
write_data=driver.find_element(By.XPATH,{self.dom_element})
write_data.send_keys("\n")
                """
            if self.wait_for is None:
                self.template=self.template
            else:
                 self.template=self.template +"\n"
                 self.template=self.template+(f"\ntime.sleep({self.wait_for})")

        return self.template.replace("/n",repr("\n"))