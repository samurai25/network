import os
import pathlib
import unittest
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service 


from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 


service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

        
class WebpageTests(unittest.TestCase):
     
    def test_title(self):
        """Make sure title is correct"""
        driver.get("http://127.0.0.1:8000/")
        self.assertEqual(driver.title, "Social Network") 
        
    def test_login(self):
        """Make sure login is correct"""
        driver.get("http://127.0.0.1:8000/login")
        username = driver.find_element(By.NAME, "username")
        password = driver.find_element(By.NAME, "password")
        login = driver.find_element(By.XPATH, "//input[@type='submit']")
        username.send_keys("Sasha")
        password.send_keys(1)
        login.click()
        self.assertEqual(driver.current_url, "http://127.0.0.1:8000/")
        
    def test_profile(self):
        """Make sure profile page is correct"""
        driver.get("http://127.0.0.1:8000/profile/Sasha/")
        
        h2 = driver.find_element(By.TAG_NAME, "h2")
        self.assertEqual(h2.text, "Profile: Sasha")
        
    def test_new_post(self):
        """Make sure new post is created"""
        driver.get("http://127.0.0.1:8000/login")
        username = driver.find_element(By.NAME, "username")
        password = driver.find_element(By.NAME, "password")
        login = driver.find_element(By.XPATH, "//input[@type='submit']")
        username.send_keys("Sasha")
        password.send_keys(1)
        login.click()
        post = driver.find_element(By.ID, "id_post")
        post_button = driver.find_element(By.XPATH, "//input[@value='Post']")
        post.send_keys("TEST")
        post_button.click()

        wait = WebDriverWait(driver, 10)
        p = wait.until(EC.visibility_of_element_located((By.XPATH, '//p[contains(text(), "TEST")]')))
    
        self.assertEqual(p.text, "TEST")
        
        
    def test_like(self):
        """Make sure like button works"""
        driver.get("http://127.0.0.1:8000/login")
        username = driver.find_element(By.NAME, "username")
        password = driver.find_element(By.NAME, "password")
        login = driver.find_element(By.XPATH, "//input[@type='submit']")
        username.send_keys("Sasha")
        password.send_keys(1)
        login.click()
        
        wait = WebDriverWait(driver, 10)
        button = wait.until(EC.visibility_of_element_located((By.XPATH, '//button[@class="bi bi-heart"]')))
        button.click()

        span = wait.until(EC.visibility_of_element_located((By.XPATH, '//span[@class="likes"]')))
       
        self.assertEqual(span.text, '1')
        
        
    def test_dislike(self):
        """Make sure dislike button works"""
        driver.get("http://127.0.0.1:8000/login")
        username = driver.find_element(By.NAME, "username")
        password = driver.find_element(By.NAME, "password")
        login = driver.find_element(By.XPATH, "//input[@type='submit']")
        username.send_keys("Sasha")
        password.send_keys(1)
        login.click()

        wait = WebDriverWait(driver, 10)
        button = wait.until(EC.visibility_of_element_located((By.XPATH, '//button[@class="bi bi-heart-fill text-danger"]')))
        button.click()
        span = wait.until(EC.visibility_of_element_located((By.XPATH, '//span[@class="likes"]')))

        self.assertEqual(span.text, '0')
        
        
        
    def test_following_page(self):
        """Test Following page."""        
        driver.get('http://127.0.0.1:8000/following')
        
        h2 = driver.find_element(By.TAG_NAME, 'h2')
        self.assertEqual(h2.text, "Following")
        
    
    def test_follow_button(self):
        """Test follow button click."""
        driver.get("http://127.0.0.1:8000/login")
        username = driver.find_element(By.NAME, "username")
        password = driver.find_element(By.NAME, "password")
        login = driver.find_element(By.XPATH, "//input[@type='submit']")
        username.send_keys("Sasha2")
        password.send_keys(2)
        login.click()

        wait = WebDriverWait(driver, 10)
        a = wait.until(EC.visibility_of_element_located((By.XPATH, '//a[contains(text(), "Alice")]')))
        a.click()
        
        follow_button = driver.find_element(By.ID, 'follow')
        follow_button.click()
        
        wait = WebDriverWait(driver, 10)
        unfollow_button = wait.until(EC.visibility_of_element_located((By.XPATH, '//button[@id="unfollow"]')))
        
        self.assertEqual(unfollow_button.text, "Unfollow")
         
      
    def test_next_page_button(self):
        # Test Next page click   
        next_btn = driver.find_element(By.XPATH, '//button[contains(text(), "Next")]')
        next_btn.click()    
        wait = WebDriverWait(driver, 10)
        a = wait.until(EC.visibility_of_element_located((By.XPATH, '//a[@class="page-link"]'))) 
        span = a.find_element(By.XPATH, '//span[contains(text(), "2")]')
        self.assertEqual(span.text, "2")
        
                
    def tear_down(self):
        driver.quit()
        
       
if __name__ == "__main__":
    unittest.main()
    
    
