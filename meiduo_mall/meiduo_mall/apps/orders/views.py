from rest_framework.response import Response
from rest_framework.views import APIView
from django_redis import get_redis_connection
from goods.models import SKU
from decimal import Decimal
from rest_framework.generics import CreateAPIView,ListAPIView

# 展示订单信息
from orders.models import OrderInfo, OrderGoods
from orders.serializers import OrderShowSerializer, OrderSaveSerializer


class OrdersShowView(APIView):

    def get(self, request):
        # 获取用户对象
        user = request.user

        # 建立redis连接
        conn = get_redis_connection('cart')
        # 获取hash数据sku_id ,count
        sku_id_count = conn.hgetall('cart_%s' %user.id) # {10:1}
        # 将byte类型数据转为整形
        cart = {}
        for sku_id, count in sku_id_count.items():
            cart[int(sku_id)] = int(count)
        # 获取集合数据
        sku_ids = conn.smembers('cart_selected_%s' %user.id)
        # 查询所有选中状态的数据对象
        skus = SKU.objects.filter(id__in=sku_ids)
        # 商品对象添加count属性(sku表中没有count字段,要手动添加属性)
        for sku in skus:
            sku.count = cart[sku.id]
        # 生成运费
        freight = Decimal(10.00)
        # 序列化返回商品对象
        ser = OrderShowSerializer({'freight': freight, 'skus': skus})
        return Response(ser.data)


# 保存订单信息
class OrderSaveView(CreateAPIView):
    serializer_class = OrderSaveSerializer


class OrdersUncommentGoodsView(ListAPIView):

    def get_queryset(self):
        # 1、获取前端数据  order_id 正则匹配
        pk = self.kwargs['pk']
        # 2、校验数据 order_id订单是否存在 不存再返回
        # SKU.objects.filter(category_id=pk)
        try:
            order = OrderInfo.objects.filter(order_id=pk)
        except:
            return Response({'error':'订单不存在'},status=400)
        # 3、判断用户登录状态 /待定，进入个人中心查看订单，此时已经登录无需验证
        # 4、根据order_id查询订单下的商品信息列表，根据信息列表获取单个商品id查询数据库
        try:
            skus = OrderGoods.objects.filter(order=pk)
        except:
            return Response({'error':'订单为空'},status=400)
        # 5、结果返回  {skus = skus}
        return Response({
            'skus':skus
        })



"""
        def get(self, request):
        # 获取前端传入的token
        token = request.query_params.get('token')
        if not token:
            return Response({'error': '缺少token'}, status=400)
        tjs = TJS(settings.SECRET_KEY, 300)
        try:
            # 检查token
            data = tjs.loads(token)
        except Exception:
            return Response({'errors': '无效token'}, status=400)
"""



