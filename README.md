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

## Project Structure
This is a simple Django project with one app called `todo`. 

I handled the DRF routing for this app's api in the main
`urls.py` file to reduce complexity with just one app. This file also handles routing for the `rest_framework_simplejwt`
views for auth.

Serializers, viewsets, and tasks are all within the `todo` app. Business logic for completing and reordering tasks were
abstracted to the `Todo` model itself.

I also added a management command called `generate_test_users` that creates a django superuser and two normal users for
quick testing.

The `uv` module's files for dep management are in the project root.

## Environment Configuration
This app relies on the use of per-environment `settings.py` files to aid in configuration across different environments.
`django-environ` was utilized to read both a `.env` file for local configuration, as well as to read env vars in cloud
deployments. The specific settings file can be configured using an env var. For this assessment, I used two settings files:
`local.py` and `production.py`. The local file reads a .env file located in the project root for local development, with
defaults set for all vars. 

Using different settings files allows us to make different selections for middleware, backends, installed apps, etc. For
example:

### local.py
- `drf-spectacular` is in `INSTALLED_APPS` to enable the Swagger API
- `SPECTACULAR_SETTINGS` are defined for Swagger
- `django.core.mail.backends.console.EmailBackend` is used to send mock test emails in the celery container

### production.py
- `drf-spectacular` is NOT in `INSTALLED_APPS` to prevent anyone from learning the API endpoints and schemas
- `SPECTACULAR_SETTINGS` are NOT defined due to the above
- `django.core.mail.backends.smtp.EmailBackend` is used as a production backend that can connect to an actual mail server
- `storages.backends.s3boto3.S3StaticStorage` is used as the storage backend to pull static files from AWS S3

Additional settings files could be created for dev/staging/demo environments along the same lines.

## Considerations
- Used `drf-spectacular` to display the API in Swagger for testing and development; much better experience than using
DRF's built in interface.
- Used `rest_framework_simplejwt` for a simple JWT auth implementation with provided `login` and `refresh_token` views.
JWT has become an industry standard and plays nice with modern frontend libs.
- Used `uv` for dependency management. I previously used `poetry` and find that `uv` offers much of the same but with
better speed and solves most of the issues I had with `poetry`. Noticeable speed up with CI/CD pipelines.
- Used `django-environ` for handling env vars in settings files. It handles using .env files locally and env vars in 
cloud deployments elegantly.

## Time Spent
I spent roughly 6.5 hours building the app and writing this README. 

The Github commit history reflects around 7.5 hours, which included a 1 hour break for dinner.