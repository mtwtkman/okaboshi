from django.conf.urls import url
from okbs.views import OKBSView


urlpatterns = [
    url(r'^$', OKBSView.as_view())
]
