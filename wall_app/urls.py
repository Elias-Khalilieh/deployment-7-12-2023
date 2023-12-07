from django.urls import path
from . import views

urlpatterns = [
    path('', views.display_log_reg),
    path('signup', views.new_sign_up),
    path('signin', views.new_sign_in),
    path('success',views.display_home),
    path('logout',views.destroysession),
    path('addmessage',views.create_msg),
    path('addcomment/<int:msgid>',views.create_cmnt),
    path('post/delete/<int:msgid>',views.delete_this_message),
    path('comment/delete/<int:cmntid>',views.delete_this_comment)
]