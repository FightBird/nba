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


class OrdersUncommentGoodsView(APIView):

    def get(self,request,order_id):
        # 1、获取前端数据  order_id 正则匹配
        # pk = self.kwargs['order_id']
        # 2、校验数据 order_id订单是否存在 不存再返回
        # SKU.objects.filter(category_id=pk)
        try:
            order = OrderInfo.objects.filter(order_id=order_id)
        except:
            return Response({'error':'订单不存在'},status=400)
        # 3、判断用户登录状态 /待定，进入个人中心查看订单，此时已经登录无需验证
        """
            # 获取前端传入的token
        # token = request.query_params.get('token')
        # if not token:
        #     return Response({'error': '缺少token'}, status=400)
        # tjs = TJS(settings.SECRET_KEY, 300)
        # try:
        #     # 检查token
        #     data = tjs.loads(token)
        # except Exception:
        #     return Response({'errors': '无效token'}, status=400)
        """
        # 4、根据order_id查询订单下的商品信息列表，根据信息列表获取单个商品id查询数据库
        try:
            skus = OrderGoods.objects.filter(order_id=order_id)
        except:
            return Response({'error':'订单为空'},status=400)
        # 5、结果返回  {skus = skus}
        skus_list = []
        for sku in skus:
            data = {
                'sku':sku.order_id,
                'price':sku.price,
                'default_image_url':sku.sku.default_image_url,
                'score':sku.score,
                'name':sku.sku.name,
                'id':sku.sku_id
            }

        return Response(data=skus_list)
    def post(self,request,atts):

        # 1、获取前端数据 order_id/sku.id/sku.comment/sku.final_score/sku.is_anonymous/token
        order_id = atts['order']
        sku_id = atts['sku']
        comment = atts['comment']
        final_score = atts['score']
        is_anonymous = atts['is_anonymous']

        # sku: sku.sku.id,
        # comment: sku.comment,
        # score: sku.final_score,
        # is_anonymous: sku.is_anonymous,
        # 2、验证数据
            # 判断用户是否登录
            # order_id查询数据库判断订单是否存在
            # sku.id查询数据库该订单 # 下是否有这商品
        goods = OrderGoods.objects.filter(order_id=order_id)
        flag = 0
        for good in goods:
            if good.order_id==order_id:
                flag = 1
                break
        if flag==0:
            return Response({'error':'商品不存在'})
        # 3、业务逻辑
        # 向数据库保存数据
        for good in goods:
            good.comment = comment
        # 对应订单商品信息表
        # 待定
        # 4、结果返回
        # ok
        return Response({
            'message':'ok'
        })


        pass

class OrderscommentGoodsView(CreateAPIView):
    def post(self, request, *args, **kwargs):
        pass

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




