# todo_drf
A simple TODO app backend using Django and DRF

## Setup
1. Run `docker-compose up` to build and run all containers (Django, Celery, Redis, Postgres). Initial DB migration is also handled here.
This will take some time, so wait until you see the Django server link message to proceed.
2Run `docker-compose exec django uv run python manage.py generate_test_users` in another shell to create a superuser 
and two test users. The superuser credentials are `admin:password`. You can view the rest of the credentials in
`todo/management/commands/generate_test_users.py` to swap between user tokens later.
3. Load the Django admin via `http://localhost:8000/admin` and enter the superuser credentials to view the DB.
4. Load the Swagger API UI via `http://localhost:8000/api/swagger/` in another tab to test the API.

## Auth
1. In the Swagger UI, locate the `POST /api/auth/login` endpoint and click the `Try it out` button to open the request form.
2. Replace the credentials with `admin:password` for the superuser, or one of the other test user's credentials. 
Click `Execute` and you will get a response with a refresh token and access token.
3. Copy the access token string, and click the `Authorize` button at the top of the page. It will prompt you to enter
the access token. Press `Authorize` and then `Close`. You are now ready to test the API (This is using JWT).

## Test API
1. You can create a new todo task by using the `POST /api/todo/` endpoint. Only text entry is allowed for the task
description. The user and position will be automatically determined upon creation. The completion state is not relevant
and will default to `False`. I suggest making a few of these to test the other endpoints. You can use the Djnago admin to
validate creation.
2. Next, test the `GET /api/todo/` and `GET /API/todo/id/` endpoints to test retrieving existing records. The former will
return all records for the authenticated user, and the latter will return a specific record by id.
3. Next, test the `PUT /api/todo/id/` and `PATCH /api/todo/id/` endpoints. These will allow you to modify the text of a
todo task. Only one field is exposed to modify, but I left the `PATCH` endpoint as it could be useful if more fields were
added at a later time.
4. Next, test the `PATCH /api/todo/reorder/id/` endpoint. You must specify a new position to move the task to.
The existing task at that position will be moved up by 1, as well as all the following tasks. You can verify the reordering
in the Django admin or using the `GET` list endpoint (results are ordered by position). NOTE: I did not add additional
validation to check if the supplied new position is an existing position or exceeds the total amount of entries.
5. Finally, test the `PATCH /api/todo/complete/id` endpoint. This will mock and email being sent using a celery task.
To view the output, you can see if in the running `docker-compose up` command, or run `docker-compose logs celery`. 
You can also clear the completion flag by sending `False` which will not send an email.