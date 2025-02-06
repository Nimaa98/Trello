from django.urls import path , include
from .views import UserView 
from rest_framework.routers import SimpleRouter




router = SimpleRouter()
router.register("account",UserView,basename="profile")




app_name = 'Account'
urlpatterns = [
        path("", include(router.urls)),

]