from django.db.models import Avg
from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from .serializers import ProductSerializer,ReviewSerializer
from rest_framework.status import *
# Create your views here.
from .filters import ProductsFilter
from .models import Product,Reviews
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

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

@api_view(['GET'])
def get_Product_By_Id(req,pk):
        product = get_object_or_404(Product,id=pk)
        serializer = ProductSerializer(instance=product)
        print(serializer.data)
        return Response(status=HTTP_200_OK,data={'Product ': serializer.data})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_product(req):
        data = req.data
        # print(f'data before serialize {data}')
        serializer=ProductSerializer(data=data)
        # print(serializer)
        if serializer.is_valid():
                #product=Product.objects.create(**data,user=req.user)
                product =serializer.save(user=req.user)
                print(product)
                res = ProductSerializer(product)
                return Response({"Product" : res.data})
        else:
                return Response(serializer.errors,status=HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_product(req,pk):
        product = get_object_or_404(Product,id=pk)
        #pser=ProductSerializer(product)
        #print(pser)
        if product.user != req.user:
                return Response({"error": "you can't update this product"},status=HTTP_403_FORBIDDEN)
        serializer = ProductSerializer(instance=product,data=req.data ,partial=True)

        if serializer.is_valid():
                serializer.save()
                print(serializer.data)
                return Response({"message":"updated done successfuly","updated_product":serializer.data},status=HTTP_200_OK)
        else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_product(req,pk):
        product = get_object_or_404(Product,id=pk)
        if product.user != req.user :
                return  Response({"error":"You can delete your own product only"},status=HTTP_400_BAD_REQUEST)
        else:
                product.delete()
                return  Response({"message","Product deleted successfully"},status=HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_review(req,product_id):
        user = req.user
        data = req.data
        product = get_object_or_404(Product,id=product_id)

        review = product.reviews.filter(user=user).first()

        if data['rating']<=0 or data['rating']>10:
                return Response({"error":"rating only between 1 to 10"},status=HTTP_400_BAD_REQUEST)
        elif review:
                serializer = ReviewSerializer(review,data=data)
                if serializer.is_valid():
                        serializer.update(instance=review,validated_data=data)
        else:
                serializer = ReviewSerializer(data=data)
                if serializer.is_valid():
                        serializer.save(user=user,product=product)

        avg_rating_dict = product.reviews.aggregate(avg_rating=Avg('rating'))
        average_rating = avg_rating_dict['avg_rating'] if avg_rating_dict['avg_rating'] is not None else 0
        product.ratings = average_rating
        product.save()

        if review:
                return Response({"details": "Product review updated"})
        else:
                return Response({'details': 'Product review created'}, status=HTTP_201_CREATED)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_review(req,product_id):
        user = req.user
        product = get_object_or_404(Product,id=product_id)

        review = product.reviews.filter(user=user).first()
        if review:
                review.delete()
                rating = product.reviews.aggregate(avg_rating = Avg('rating'))
                product.ratings = rating['avg_rating'] if rating['avg_rating'] is not None else 0
                product.save()
                return Response({'details':'product review deleted'},status=HTTP_200_OK)
        else:
                return Response({'error':'product review not found'},status=HTTP_404_NOT_FOUND)