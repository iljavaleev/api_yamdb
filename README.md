# Проект YaMDb-api
##### Групповой проект Яндекс.Практикум | Программа python-разработчики | Спринт 10
---

### Авторы проекта

[Илья Валеев](https://github.com/iljavaleev/) | [Александ Лахтюк](https://github.com/aslakhtyuk/) | [Дмитрий Кирсанов](https://github.com/vepsong/)


---
## О проекте YaMDb

Проект YaMDb собирает отзывы пользователей на произведения.

Произведения делятся на категории: «Книги», «Фильмы», «Музыка».
    
Список категорий может быть расширен администратором (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»).

Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

В каждой категории есть произведения: книги, фильмы или музыка. Например, в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Насекомые» и вторая сюита Баха.

Произведению может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). Новые жанры может создавать только администратор.

Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). 

На одно произведение пользователь может оставить только один отзыв.

---

## Используемые технологии

* Django REST Framework
* Simple-JWT

## Основные endpoint'ы

* signup — регистрация пользователя и получение электронного письма с кодом подтверждения.
* token — получение токена для аутентификации пользователя.
* users — работа с пользователями.
* categories — работа с категориями.
* genres — работа с жанрами.
* titles — работа с произведениями.
* rewies — работа с отзывами.
* comments — работа с комментариями.

Подробный список всех endpoint'ов и примеры ответов в [техническом задании](#Техническое-задание)

## Техническое задание

Техническое задание доступно по адресу: 
http://127.0.0.1:8000/redoc

p.s. ссылка активна только при запущенном тестовом сервере.

## Инструкция по запуску проекта на локальной машине

Все операции выполняются в командной строке.


* Клонировать репозиторий:
```
git clone <ссылка>
```
* Создать и активировать вирутальное окружение:
```
python -m venv env
```
* Установить зависимости из файла requirements.txt:
```
python -m pip install --upgrade pip 
pip install -r requirements.txt
```
* Выполнить миграции:
```
python manage.py makemigrations
python manage.py migrate
```
* Запустить тестовый сервер:
```
python manage.py runserver
```

## Авторы проекта
[Илья Валеев](https://github.com/iljavaleev/) | [Александ Лахтюк](https://github.com/aslakhtyuk/) | [Дмитрий Кирсанов](https://github.com/vepsong/)