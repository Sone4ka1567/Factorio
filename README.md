# ENDustrial

[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/)
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>

## Описание

ENDustial - экономический симулятор с элементами пошаговой стратегии,
вдохновленный [factorio](https://www.factorio.com/). Игроку нужно автоматизировать добычу ресурсов, строить
перерабатывающие машины и производить различные материалы.

## Прогресс

На данный момент (21 марта) написаны классы Карт мира (есть два вида: простая и сложная), и реализованы фабричный метод
для создания Карты. Также создан класс игрока (Player) и начата реализация камеры.

## UML

UML-диаграмма общей структуры в файле overall-structure.png и [здесь](https://app.creately.com/diagram/gmXmNSb8s2E/) (
нужна регистрация).  
UML-диаграмма ресурсов ("из чего что делается") в resources-tree.png

## Паттерны

[Фабричный метод для создания карт](https://github.com/EgorVoron/patterns-project/blob/41cb173b12fd55de069cbb7a62a914fa5a2ab905/maps.py#L117)  
[Фасад для pyGame](https://github.com/EgorVoron/patterns-project/blob/41cb173b12fd55de069cbb7a62a914fa5a2ab905/facade.py#L4)  
[Компоновщик](https://github.com/EgorVoron/patterns-project/blob/d6d463bf2bf32fd37060a9491a44a363ae6d83a5/core/virtual_objects/materials/abstracts.py#L36)
*(нужен для построения и прохода по дереву зависимостей ресурса)*
[Proxy](https://github.com/EgorVoron/patterns-project/blob/d6d463bf2bf32fd37060a9491a44a363ae6d83a5/core/map_objects/abstracts.py#L5)
*(для подсчета прогресса в тиках)*
