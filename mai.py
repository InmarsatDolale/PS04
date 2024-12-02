from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    return driver


def search_article(driver, query):
    base_url = "https://ru.wikipedia.org/wiki/"
    driver.get(base_url)
    search_box = driver.find_element(By.NAME, "search")
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)
    if "wikipedia.org/wiki/" in driver.current_url:
        return driver.current_url
    try:
        first_result = driver.find_element(By.CSS_SELECTOR, ".mw-search-result a")
        return first_result.get_attribute("href")
    except:
        return None


def display_paragraphs(driver):
    paragraphs = driver.find_elements(By.CSS_SELECTOR, "p")
    index = 0
    while index < len(paragraphs):
        print(f"\nПараграф {index + 1} из {len(paragraphs)}:\n")
        print(paragraphs[index].text)
        print("\nЧто дальше?")
        print("1: Следующий параграф")
        print("2: Предыдущий параграф")
        print("3: Вернуться в меню")
        choice = input("Выберите действие (1/2/3): ").strip()
        if choice == "1" and index < len(paragraphs) - 1:
            index += 1
        elif choice == "2" and index > 0:
            index -= 1
        elif choice == "3":
            break
        else:
            print("Некорректный ввод. Попробуйте снова.")


def display_links(driver):
    links = driver.find_elements(By.CSS_SELECTOR, "#bodyContent a")
    internal_links = [link for link in links if '/wiki/' in link.get_attribute("href")]
    for i, link in enumerate(internal_links, 1):
        print(f"{i}. {link.text or link.get_attribute('href')}")
    print("0. Вернуться в меню")
    return internal_links


def wikipedia_browser():
    driver = setup_driver()
    print("Добро пожаловать в Википедия-браузер!")

    try:
        while True:
            query = input("\nВведите ваш запрос (или 'выход' для завершения): ").strip()
            if query.lower() == 'выход':
                print("До свидания!")
                break

            article_url = search_article(driver, query)
            if not article_url:
                print("Статья не найдена. Попробуйте снова.")
                continue

            driver.get(article_url)
            print(f"\nСтатья: {driver.title}")
            print("1: Листать параграфы статьи")
            print("2: Перейти к связанным статьям")
            print("3: Выйти из программы")

            choice = input("Выберите действие (1/2/3): ").strip()
            if choice == "1":
                display_paragraphs(driver)
            elif choice == "2":
                while True:
                    links = display_links(driver)
                    choice = input("Введите номер связанной статьи (или 0 для возврата): ").strip()
                    if choice == "0":
                        break
                    elif choice.isdigit() and 1 <= int(choice) <= len(links):
                        selected_link = links[int(choice) - 1]
                        driver.get(selected_link.get_attribute("href"))
                        print(f"\nСтатья: {driver.title}")
                        print("1: Листать параграфы статьи")
                        print("2: Перейти к связанным статьям")
                        print("3: Вернуться в меню")
                        sub_choice = input("Выберите действие (1/2/3): ").strip()
                        if sub_choice == "1":
                            display_paragraphs(driver)
                        elif sub_choice == "2":
                            continue
                        elif sub_choice == "3":
                            break
                        else:
                            print("Некорректный ввод.")
                    else:
                        print("Некорректный выбор. Попробуйте снова.")
            elif choice == "3":
                print("До свидания!")
                break
            else:
                print("Некорректный ввод. Попробуйте снова.")
    finally:
        driver.quit()


if __name__ == "__main__":
    wikipedia_browser()