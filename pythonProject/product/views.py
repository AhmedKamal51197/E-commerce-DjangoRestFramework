from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProductSerializer
from rest_framework.status import *
# Create your views here.
from .filters import ProductsFilter
from .models import Product
from rest_framework.pagination import PageNumberPagination
@api_view(['GET'])
def get_all_products(req):

        #products = Product.objects.all()
        filterSet= ProductsFilter(req.GET,queryset=Product.objects.all().order_by('id'))
        respage=2
        count = filterSet.qs.count()
        paginator = PageNumberPagination()
        paginator.page_size=respage
        queryset = paginator.paginate_queryset(filterSet.qs,req)
        print(filterSet.data)
        if not filterSet.qs.exists():#products.exists():
                return Response(status=HTTP_200_OK,data={"msg":"No products existing"})
        else :
                # serializer = ProductSerializer(instance=products,many=True)
                serializer = ProductSerializer(instance=queryset,many=True)
                return Response(status=HTTP_200_OK,data={'products':serializer.data,'page number':req.query_params.get('page',1),'pages count':(int)(count/respage),'per page':respage,'count_of_all_products':count})

@api_view(['GET'])
def get_Product_By_Id(req,pk):
        product = get_object_or_404(Product,id=pk)
        serializer = ProductSerializer(instance=product)
        print(serializer.data)
        return Response(status=HTTP_200_OK,data={'Product ': serializer.data})