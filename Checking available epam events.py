import requests
from bs4 import BeautifulSoup

base_url = "https://training.epam.com/en/training/"

for i in range(1, 10000):
    page_number = f"{i:04d}"
    url = base_url + page_number
  
    response = requests.get(url)

    if response.status_code == 200:
      
        soup = BeautifulSoup(response.content, "html.parser")
        title = soup.title.text if soup.title else "Нет заголовка"
        print(f"Страница {url} имеет заголовок: {title}")
    elif response.status_code == 404:
        print(f"Ошибка 404: Страница {url} не найдена")
    elif response.status_code == 403:
        print(f"Ошибка 403: Доступ запрещен к странице {url}")
    else:
        print(f"Ошибка {response.status_code} при доступе к странице {url}")
