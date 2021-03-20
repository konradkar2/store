Game Store backend
==
This project is the backend restfull app for https://github.com/Matt444/GameStore--frontend/
**API description** at https://app.swaggerhub.com/apis/konradkar2/store/1.0.0

About
---
Our main task was to implement "complex" relational database and some interface to it, so we have come with an idea to make a web store that sells games.

![](https://user-images.githubusercontent.com/64275057/111546638-4518a380-8778-11eb-901b-db8a95ea12fa.png)
Database
--
We have decided for MySQL as the database
Here you can see it's structure
![](https://github.com/konradkar2/store/blob/main/database_structure.PNG?raw=true)

Features
--
- We used python and flask restful
- All quaries consist of pure sql commands, no ORM was used
- SQL queries are safe, we've implemented transactions and no SQL injection is possible
- all the endpoints and their description are available at the link to swagger on top of readme.

Creators
--
Konrad Karaś https://github.com/konradkar2
Jakub Bekier https://github.com/JakubBekier
Mateusz Joniec https://github.com/Matt444
