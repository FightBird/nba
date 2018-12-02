from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^orders/settlement/$', views.OrdersShowView.as_view()),
    url(r'^orders/$', views.OrderSaveView.as_view()),

    # '/orders/'+this.order_id+'/uncommentgoods/'
    url(r'^orders/(?P<order_id>\d+)/uncommentgoods/$', views.OrdersUncommentGoodsView.as_view()),
    # url(r'^orders/(?P<order_id>\d+)/uncommentgoods/$', views.OrdersUncommentGoodsView.as_view()),
    # orders/2018120211491543722554000000001/uncommentgoods//goods_judge.html?order_id=' + order.order_id

]