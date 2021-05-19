# Cornerlunch 

Cornerlunch is an application that allows the coordination of food deliveries to Cornershop employees in each country using Django, DRF and Celery

## Introduction

### Technical aspects
For the correct deployment of the project, the following actions are necessary.
1. Assign an environment variable 'SLACK_BOT_TOKEN' with the value of your 'Bot User OAuth Token' from slack
2. Install the 'slack-sdk' and 'django-filter' plugins found at the end of the 'requirements.text' file

### Features
1. List, Create and Modify the menus of each country where Cornershop has employees and delimiting with a time limit to place a lunch order
2. List, Create and Modify the dishes that are part of the daily menus, these can be new or already created in order to give the possibility of creating statistics on the consumption of dishes in the future and be a tool capable of influencing business decisions such as remove or add new food concepts
3. List, Create and Modify employees by assigning their country and Slack identifier
4. Publish menus to employees via private message to their Slack user asynchronously
5. Allows employees, through a link with uuid code, to choose their favorite dishes and customizations without having to spend time on authentications, since each link is unique by menu and employee

### API Guide
| URL Pattern | HTTP Method | Action |
| - | - | - |
|/api/order/?menu={int:menu_id} | GET | Order list |
|/api/order/| GET | Detail of an order |
|/api/order/{uuid:id}/| PATCH | Choosing favorite dishes |
|/api/menu/| GET | Menu list |
|/api/menu/{int:id}/| GET | Menu detail |
|/api/menu/| POST | Creating a menu |
|/api/menu/{int:id}/| PATCH | Modifying a menu |
|/api/menu/{int:id}/publish/| POST | Publishing a menu |
|/api/dish/| GET | List of dishes |
|/api/dish/{int:id}/| GET | Dish detail |
|/api/dish/| POST | Creating a dish |
|/api/dish/{int:id}/| PATCH | Modifying a dish |
|/api/employee/| GET | List employees |
|/api/employee/{int:id}/| GET | Employee detail |
|/api/employee/| POST | Creation of an employee |
|/api/employee/{int:id}/| PATCH | Modification of an employee |


### ABC of the web application
1. Create a user with '$ python manage.py createsuperuser'
2. Login at http://127.0.0.1:8000/
3. Click on the 'Employees' link and on 'Create a new employee'
4. Assign a valid Slack id and make sure the bot user can send private messages
5. Click on the 'Dishes' link and on 'Create a new dish'
6. Create at least one dish of each type
7. Click on the link 'Menus' and on 'Create a new menu'
8. Assign the dishes corresponding to that menu and choose the same country as the previous employee
9. Return to the link 'Menu'
10. Press the 'Send notifications' button
11. The message will reach the user slack and must enter through the following link http://127.0.0.1:8000/menu/{uuid}
12. Choose your favorite dishes

! [slack message example](cornershop-backend-test/docs/slack-message.png)

### Tests
Run '$ python manage.py apps.menu.tests'

## Deployment
From the following folder (cornershop-backend-test), run these commands

### Running the development environment
* `make up`
* `dev up`

##### Rebuilding the base Docker image
* `make rebuild`

##### Resetting the local database
* `make reset`

### Hostnames for accessing the service directly
* Local: http://127.0.0.1:8000