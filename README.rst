==================
Вариант 7 задание
==================
| 
| Визуализация цен недвижимости
|
| 1) Найти (crawling с сайтов недвижимости) актуальную базу данных по стоимости недвижимости в Санкт-Петербурге, Москве, Екатеринбурге
|
| 2) На основе собранных данных сделать следующие виды визуализации:
|     a) тепловая карта цен недвижимости. Представляет из себя карту города с наложенным на неё слоем, в котором цветом показана цена недвижимости в пересчёте на квадратный метр.
|     б) Гистограмма с отображением средних цен по муниципальным округам указанных выше городов
|     в) Гистограмма с отображением средней площади квартиры по муниципальным округам указанных выше городов
|
| Под визуализацией понимается png картинка с достаточным разрешением. При желании это может быть так же web frontend или оконное приложение.

=====================
Heatmap and histogram
=====================
| For application to work googlemaps api key is needed pass it to heatmap/management/commands/get_locations 55 line
| and to templates/heatmap.html 46 line
|
| 1 To create virtual environment run python3 -m venv venv
|
| 2 To activate it run .\\venv\\Scripts\\activate
|
| 3 Run pip install -r requirements.txt to install all dependencies
|
| 4 To run server run command python3 manage.py runserver
|
| 5 To get needed histogram run command 'python manage.py create_histogram --city --data'
|    options: to get information for city pass one of this options: spb, ekb, msk
|        to get certain type of data pass option: price, area
|        price will give you histogram based on average prices for regions in specified city
|        area will give you histogram based on average areas for regions in specified city
|
| 6 To collect data from website run 'python manage.py scraper --city' Parsed information will be saved in site_data/parsed_site_data folder
|
| 7 To get detailed information for every address after scraper run 'python manage.py get_locations --city' For this to work you need an API key for Google geocoder. Result will be saved to site_data/locations folder
