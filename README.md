# PROJECT GEOCatalog

Тестовое задание.
	
	Требуется создать python веб-сервис. В качестве основы необходимо использовать один из веб-фреймворков: flask(предпочтительно), FastAPI, aiohttp. Django желательно не использовать.
	Сервис должен предоставлять возможность редактирования регионов и городов, которые входят в регионы.
	Регионы – древовидная структура (имеется поле parent_id, которые ссылается на id)
	Города – плоская структура, в которой имеется ссылка на регион.
	Сервис должен предоставлять методы:
	1. управления справочником регионов: добавление/изменение/удаление
	2. просмотр всех регионов в виде дерева
	3. просмотр городов в виде списка. Входной параметр:
		region_id. Если он передан – возвращаются только города из этого региона или всех дочерних к нему регионов.
	Выходные данные из сервиса должны быть в json-формате
	Данные по городам, регионам и пользователям должны храниться в реляционой БД. Доступ из сервиса к ним необходимо осуществлять через ORM.

## Requirements

Python modules:
Flask==1.1.4
psycopg2==2.8.4
SQLAlchemy==1.3.17

## API Methods

- GET /regions/ - просмотр всех регионов в виде дерева
- POST /regions/ - Создание региона. В теле запроса json вида
	{
		"name": "Москвская область",
		"parent_id": 12
	}
parent_id не обязательный

- GET /regions/{region_id}/ - Просмотр региона. Выводит список городов и дочерних регионов
- PUT /regions/{region_id}/ - Редактировани региона. В теле запроса json вида
	{
		"name": "Москвская область",
		"parent_id": 12
	}
parent_id не обязательный. Если не передан, то регион становится регионом верхнего уровня

- DELETE /regions/{region_id}/ - Удаление региона.
- GET /regions/{region_id}/cities/ - Просмотр городов региона. Возвращаются только города из этого региона или всех дочерних к нему регионов.
- POST /regions/{region_id}/cities/ - Созднание города в регионе region_id. В теле запроса json вида
	{
		"name": "Москвская область",
	}
- PUT /regions/{region_id}/cities/{city_id}/ - Редактирование города в регионе region_id. В теле запроса json вида
	{
		"name": "Москвская область",
		"region_id": 21
	}
Если передан параметр region_id, то городу изменится регион

- DELETE /regions/{region_id}/cities/{city_id}/ - Удаление города
