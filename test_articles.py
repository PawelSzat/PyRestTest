import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

@pytest.fixture
def driver():
    driver = webdriver.Chrome()  # Upewnij się, że ChromeDriver jest zainstalowany i w PATH
    yield driver
    driver.quit()  # Zamykanie przeglądarki po zakończeniu testu

def test_create_article(driver):
    driver.get("http://localhost:8081")  # Zmień URL, jeśli to konieczne
    print("Otwieram stronę do tworzenia artykułu...")

    try:
        print("Czekam na możliwość wypełnienia formularza...")
        WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.NAME, "title"))
        )
    except TimeoutException:
        print("Timed out waiting for the 'title' input to be visible")
        driver.quit()
        raise

    # Uzupełnij formularz tworzenia artykułu
    print("Wypełniam formularz w tytule...")
    driver.find_element(By.NAME, "title").send_keys("New article")
    print("Wypełniam formularz w treści...")
    driver.find_element(By.NAME, "content").send_keys("Text example")
    print("Klikam przycisk do stworzenia artykułu...")
    driver.find_element(By.ID, "create-button").click()

    try:
        print("Czekam na komunikat o utworzeniu artykułu...")
        WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, "//div[contains(text(), 'Artykuł został utworzony')]"))
        )
    except TimeoutException:
        print("Timed out waiting for the success message to appear")
        driver.quit()
        raise
    
    assert "Artykuł został utworzony" in driver.page_source

def test_edit_article(driver):
    driver.get("http://localhost:8081/articles/1/edit")  # Zmień URL, aby przejść do edycji artykułu
    print("Otwieram stronę do edytowania artykułu...")

    try:
        print("Czekam na formularz edycji...")
        WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.NAME, "title"))
        )
    except TimeoutException:
        print("Timed out waiting for the 'title' input to be visible")
        driver.quit()
        raise
    
    driver.find_element(By.NAME, "title").clear()  # Wyczyść pole tytułu
    driver.find_element(By.NAME, "title").send_keys("New article v2")
    driver.find_element(By.NAME, "content").clear()  # Wyczyść pole treści
    driver.find_element(By.NAME, "content").send_keys("Text article v2")
    print("Klikam przycisk do zapisania edytowanego artykułu...")
    driver.find_element(By.ID, "save-button").click()  # Przyciski mogą mieć inne identyfikatory

    try:
        print("Czekam na komunikat, że artykuł został zaktualizowany...")
        WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, "//div[contains(text(), 'Artykuł został zaktualizowany')]"))
        )
    except TimeoutException:
        print("Timed out waiting for the updated message to appear")
        driver.quit()
        raise
    
    assert "Artykuł został zaktualizowany" in driver.page_source

def test_delete_article(driver):
    driver.get("http://localhost:8081/articles/1")  # Zmień URL, aby przejść do detali artykułu
    print("Otwieram stronę do usuwania artykułu...")

    try:
        print("Czekam na przycisk do usunięcia artykułu...")
        WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, "//button[contains(text(), 'DELETE')]"))
        )
    except TimeoutException:
        print("Timed out waiting for the delete button to be visible")
        driver.quit()
        raise

    # Kliknij przycisk usunięcia
    driver.find_element(By.XPATH, "//button[contains(text(), 'DELETE')]").click()

    try:
        WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, "//div[contains(text(), 'Artykuł został usunięty')]"))
        )
    except TimeoutException:
        print("Timed out waiting for the deletion message to appear")
        driver.quit()
        raise

    assert "Artykuł został usunięty" in driver.page_source
