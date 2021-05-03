# ENDustrial

[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/)
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>

## Описание

ENDustial - экономический симулятор с элементами пошаговой стратегии,
вдохновленный [factorio](https://www.factorio.com/). Игроку нужно автоматизировать добычу ресурсов, строить
перерабатывающие машины и производить различные материалы.

## Запуск

```
python main_loop.py
```

## Прогресс

На данный момент (4 мая) в ядре (core) готовы ресурсы, производящие их машины и элементы электрических цепей, в графике
реализовано меню (крутой дизайн будет позже), отрисовка карты, рудников и деревьев на ней, а так же камера, игрок и
реализовано управление им клавишами wasd.

## UML

UML-диаграммы:
[общая структура](https://app.creately.com/diagram/gmXmNSb8s2E/)  
[дерево ресурсов](https://app.creately.com/diagram/Ppx7fkEvcIh/edit)  
[дерево с машинами](https://app.creately.com/diagram/mYLUvGOoPj5/edit)

*(Мы правда стараемся их обновлять, но скорость прогресса в разработке сильно превышает скорость рисования красивеньких
UML'ек)*

## Паттерны

[Фабричный метод для создания карт](https://github.com/EgorVoron/patterns-project/blob/ea5dcf1605d6902331cbbe003e43c4f69998071d/maps.py#L98)  
[Фасад для pyGame](https://github.com/EgorVoron/patterns-project/blob/ea5dcf1605d6902331cbbe003e43c4f69998071d/facade.py#L4)  
[Компоновщик](https://github.com/EgorVoron/patterns-project/blob/ea5dcf1605d6902331cbbe003e43c4f69998071d/core/virtual_objects/materials/abstracts.py#L42)
*(нужен для построения и прохода по дереву зависимостей ресурса)*  
[Мост](https://github.com/EgorVoron/patterns-project/blob/dev/core/map_objects/production)
*("абстракция" - Machine, "реализация" - PowerSource)*  
[Proxy](https://github.com/EgorVoron/patterns-project/blob/dev/core/map_objects/abstracts.py)
*(будет нужен для подсчета прогресса в тиках)*  
От декоратора отказались, поскольку в нашей игре нет такого понятия как "апгрейд" объекта - поведение всех объектов
заранее определено. В некотором смысле вместо него используется Мост для того, чтоб не делать множественное
наследование.
