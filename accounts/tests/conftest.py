import pytest


@pytest.fixture(autouse=True)
def reset_celery_task_queues_between_tests(celery_app):
    celery_app.control.purge()
