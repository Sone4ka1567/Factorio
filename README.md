# ENDustrial

[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/)
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>

## Разработчики
Sone4ka1567 и EgorVoron

## Описание

ENDustial - экономический симулятор с элементами пошаговой стратегии,
вдохновленный [factorio](https://www.factorio.com/). Игроку нужно автоматизировать добычу ресурсов, строить
перерабатывающие машины и производить различные материалы.

## Запуск

```
python main_loop.py
```

## Прогресс

На данный момент (17 мая) в ядре (core) готовы ресурсы, производящие их машины и элементы электрических цепей, в графике
реализованы: меню, постановка и уборка машин, взаимодействие с машинами и производство материалов.

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
[Цепочка обязанностей](https://github.com/EgorVoron/patterns-project/blob/8c26ee0c013d728448bb9bfb4e3122f37f8eb8aa/core/safe_creator.py#L5) *(
нужен для обработки ошибок при взаимодействии с картой)*  
[Модифицированный наблюдатель](https://github.com/EgorVoron/patterns-project/blob/8c26ee0c013d728448bb9bfb4e3122f37f8eb8aa/core/map_objects/production/electricity.py#L26)
*(Для взаимодействия электрических столбцов)*

## Инструкция

Для перемещения используйте клавиши `wasd`, для открытия рюкзака `e`, для закрытия - `esc`  
Ваша задача — построить радар для связи с большой землей. Для этого вам понадобится добыть очень много ресурсов, а
количество ходов ограниченно, поэтому, чтобы ускорить этот процесс, необходимо строить добывающие и перерабатывающие
машины. Для того чтобы добывать ресурс из клетки, нажмите правую кнопку мыши, а для установки машины в данную клетку —
левую. Для ручного создания машины в рюкзаке зайдите в рюкзак и в правом разделе выберите машину. Для установки машины
на карту нажмите на нужную клетку и выберите машину из левой части рюкзака. Для взаимодействия с машиной нажмите левой
кнопкой на машину. Для того чтобы убрать машину, нажмите правой мышкой на нее.
