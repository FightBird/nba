from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^orders/settlement/$', views.OrdersShowView.as_view()),
    url(r'^orders/$', views.OrderSaveView.as_view()),

    # '/orders/'+this.order_id+'/uncommentgoods/'
    url(r'^orders/(?P<pk>\d+)/uncommentgoods/$', views.OrdersUncommentGoodsView.as_view()),

]