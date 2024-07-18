from django.urls import path
from task_manager.views import (
    index,
    TaskTypeListView,
    TaskTypeCreateView,
    TaskTypeUpdateView,
    TaskTypeDeleteView,
    WorkerListView,
    WorkerCreateView,
    WorkerUpdateView,
    WorkerDeleteView,
    WorkerDetailView,
    PositionListView,
    PositionCreateView,
    PositionUpdateView,
    PositionDeleteView,
    TaskListView,
    TaskDetailView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
)

urlpatterns = [
    path("", index, name="index"),
    path("task_type/", TaskTypeListView.as_view(), name="task_type-list"),
    path(
        "task_type/create/",
        TaskTypeCreateView.as_view(),
        name="task-type-create"
    ),
    path(
        "task_type/<int:pk>/update/",
        TaskTypeUpdateView.as_view(),
        name="task-type-update"
    ),
    path(
        "task_type/<int:pk>/delete/",
        TaskTypeDeleteView.as_view(),
        name="task-type-delete"
    ),
    path(
        "positions/",
        PositionListView.as_view(),
        name="position-list"
    ),
    path(
        "positions/create/",
        PositionCreateView.as_view(),
        name="position-create"
    ),
    path(
        "positions/<int:pk>/update/",
        PositionUpdateView.as_view(),
        name="position-update"
    ),
    path(
        "positions/<int:pk>/delete/",
        PositionDeleteView.as_view(),
        name="position-delete"
    ),
    path("workers/", WorkerListView.as_view(), name="worker-list"),
    path(
        "workers/<int:pk>/", WorkerDetailView.as_view(), name="worker-detail"
    ),
    path("workers/create/", WorkerCreateView.as_view(), name="worker-create"),
    path(
        "workers/<int:pk>/update/",
        WorkerUpdateView.as_view(),
        name="worker-update"
    ),
    path(
        "workers/<int:pk>/delete/",
        WorkerDeleteView.as_view(),
        name="worker-delete"
    ),
    path(
        "tasks/",
        TaskListView.as_view(),
        name="task-list"
    ),
    path(
        "task/<int:pk>/detail/",
        TaskDetailView.as_view(),
        name="task-detail"
    ),
    path(
        "task/create/",
        TaskCreateView.as_view(),
        name="task-create"
    ),
    path(
        "task/update/",
        TaskUpdateView.as_view(),
        name="task-update"
    ),
    path(
        "task/delete/",
        TaskDeleteView.as_view(),
        name="task-delete"
    ),
]

app_name = "task_manager"
