# ENDustrial

[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/)

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
