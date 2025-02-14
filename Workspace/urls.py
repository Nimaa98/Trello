from django.urls import path , include
from .views import WorkspaceView,BoardView,ProjectView,TaskView,RoleView,WorkspaceUserView
from rest_framework.routers import SimpleRouter



workspace_router = SimpleRouter()
workspace_router.register("workspace",WorkspaceView,basename="workspace")

board_router = SimpleRouter()
board_router.register("board",BoardView,basename="board")

project_router = SimpleRouter()
project_router.register("project",ProjectView,basename="project")

task_router = SimpleRouter()
task_router.register("task",TaskView,basename="task")

role_router = SimpleRouter()
role_router.register("role",RoleView,basename="role")

workspace_user_router = SimpleRouter()
workspace_user_router.register("workspaceuser",WorkspaceUserView,basename="workspaceuser")



app_name = 'Workspace'
urlpatterns = [
        path("", include(workspace_router.urls)),
        path("", include(board_router.urls)),
        path("", include(project_router.urls)),
        path("", include(task_router.urls)),
        path("", include(role_router.urls)),
        path("", include(workspace_user_router.urls)),

]