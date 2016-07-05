from django.conf.urls import url

from cgi_wrap_test_app import views

urlpatterns = [
    url(r'^example_cgi$', views.example_cgi),
    url(r'^example_cgi_with_args$', views.example_cgi_with_args),
]
