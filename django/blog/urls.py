from django.urls import path
from blog import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('token/', views.token, name='token'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('article/', views.article, name='article'),
    path('article/<int:article_id>/', views.article_id, name='article_id'),
    path('article/<int:article_id>/comment/', views.comment, name='comment'),
    path('comment/<int:comment_id>/', views.comment_id, name='comment_id'),
]
