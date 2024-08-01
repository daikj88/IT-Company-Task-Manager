from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_manager.models import TaskType, Position

TASKTYPE_URL = reverse("task_manager:task-type-list")


class PublicTaskTypeTest(TestCase):
    def test_login_required(self):
        res = self.client.get(reverse("task_manager:task-type-list"))
        self.assertNotEqual(res.status_code, 200)

class PrivateTaskTypeTest(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="test_position")
        self.user = get_user_model().objects.create_user(
            username="test_username",
            password="test123",
            position=self.position
        )
        self.client.force_login(self.user)
        self.task_type = TaskType.objects.create(name="test_task_type")

    def test_retrieve_task_type(self):
        res = self.client.get(reverse("task_manager:task-type-list"))
        self.assertEqual(res.status_code, 200)
        task_types = TaskType.objects.all()
        self.assertEqual(
            list(res.context["task_types_list"]),
            list(task_types)
        )

    def test_search_task_type(self):
        res = self.client.get(reverse("task_manager:task-type-list") + "?name=test_task_type")
        task_type = TaskType.objects.filter(name__icontains="test_task_type")
        self.assertEqual(
            list(res.context["task_types_list"]),
            list(task_type)
        )

    def test_create_task_type(self):
        response = self.client.post(
            reverse("task_manager:task-type-create"),
            {"name": "new_task_type"}
        )
        self.assertRedirects(response, reverse("task_manager:task-type-list"))
        self.assertTrue(
            TaskType.objects.filter(name="new_task_type").exists()
        )

    def test_update_task_type(self):
        task_type_id = self.task_type.pk
        res = self.client.post(
            reverse("task_manager:task-type-update", args=[task_type_id]),
            {"name": "updated_task_type"}
        )
        self.assertRedirects(res, reverse("task_manager:task-type-list"))
        self.assertTrue(
            TaskType.objects.filter(name="updated_task_type").exists()
        )

    def test_delete_task_type(self):
        task_type_id = self.task_type.pk
        response = self.client.post(
            reverse("task_manager:task-type-delete", args=[task_type_id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            TaskType.objects.filter(id=task_type_id).exists()
        )