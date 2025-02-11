from rest_framework import routers
from .views import DibujoViewset

app_name = 'api'
router = routers.DefaultRouter()
router.register('dibujo', DibujoViewset, 'dibujo_api')

urlpatterns = router.urls