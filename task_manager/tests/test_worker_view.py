from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_manager.models import Position

WORKER_URL = reverse("task_manager:worker-list")


class PublicWorkerTest(TestCase):
    def test_login_required(self):
        res = self.client.get(WORKER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateWorkerTest(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="test_position")
        self.update_position = Position.objects.create(name="update_position")
        self.user = get_user_model().objects.create_user(
            username="test_username",
            password="test123",
            position=self.position
        )
        self.client.force_login(self.user)

    def test_retrieve_workers(self):
        res = self.client.get(WORKER_URL)
        self.assertEqual(res.status_code, 200)
        workers = get_user_model().objects.all()
        self.assertEqual(
            list(res.context["worker_list"]),
            list(workers)
        )
        self.assertTemplateUsed(
            res,
            "task_manager/worker_list.html"
        )

    def test_search_workers(self):
        res = self.client.get(WORKER_URL + "?username=test_username")
        worker = get_user_model().objects.filter(username__icontains="test_username")
        self.assertEqual(
            list(res.context["worker_list"]),
            list(worker)
        )

    def test_detail_worker(self):
        worker_id = self.user.id
        res = self.client.get(reverse("task_manager:worker-detail", args=[worker_id]))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "task_manager/worker_detail.html")

    def test_create_worker(self):
        response = self.client.post(
            reverse("task_manager:worker-create"),
            {
                "username": "new_username",
                "password1": "new_password",
                "password2": "new_password",
                "position": self.position.id,
                "first_name": "John",
                "last_name": "Doe",
            }
        )
        self.assertRedirects(response, reverse("task_manager:worker-list"))
        self.assertTrue(
            get_user_model().objects.filter(username="new_username").exists()
        )

    def test_update_worker(self):
        worker_id = self.user.id
        res = self.client.post(
            reverse("task_manager:worker-update", args=[worker_id]),
            {
                "first_name": "update_name",
                "last_name": "update_lastname",
                "position": self.update_position.id,
                "username": "update_username",
                "email": "update_email@gmail.com",
            }
        )
        self.assertRedirects(res, reverse("task_manager:worker-list"))
        updated_worker = get_user_model().objects.get(id=worker_id)
        self.assertEqual(updated_worker.username, "update_username")
        self.assertEqual(updated_worker.position, self.update_position)
        self.assertEqual(updated_worker.email, "update_email@gmail.com")
        self.assertEqual(updated_worker.first_name, "update_name")
        self.assertEqual(updated_worker.last_name, "update_lastname")

    def test_delete_worker(self):
        worker_id = self.user.id
        response = self.client.post(
            reverse("task_manager:worker-delete", args=[worker_id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            get_user_model().objects.filter(id=worker_id).exists()
        )