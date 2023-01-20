from django.urls import path

from . import views

app_name = 'main'

urlpatterns = [
    path("", views.home, name='home'),
    path("<int:thread_id>/", views.thread_view, name="thread_view"),
    path("<int:thread_id>/vote/", views.thread_vote, name="thread_vote"),
    path("<int:thread_id>/comments/add", views.add_comment, name="add_comment"),
    path("<int:thread_id>/comments/", views.thread_comment_view, name="thread_comments"),
    path("<int:thread_id>/delete", views.delete_thread, name="delete_thread"),
    path("post/", views.post_thread, name="post_thread"),
    path("accounts/signup/", views.sign_up, name="sign_up"),
    path("thread_deleted/", views.thread_deleted, name="thread_deleted")


]

