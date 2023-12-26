from django.urls import path
from attendance import views
urlpatterns = [
    path('',views.index,name='index'),
    path('convert',views.convert,name='convert'),
    # path('download',views.download_excel,name='download')
]
