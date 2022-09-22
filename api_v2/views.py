import json

from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from api_v2.serializers import ArticleSerializer
from webapp.models import Article


class ArticleListView(APIView):
    def get(self, request, *args, **kwargs):
        objects = Article.objects.all()
        serializer = ArticleSerializer(objects, many=True)
        return Response(serializer.data)


class ArticleDetailView(APIView):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        article = Article.objects.get(id=pk)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)


class ArticleCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=201)


class ArticleUpdateView(APIView):
    def put(self, request, pk, *args, **kwargs):
        article = get_object_or_404(Article, pk=pk)
        if request.body:
            body = json.loads(request.body)
            serializer = ArticleSerializer(data=body, instance=article)
            try:
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return JsonResponse(serializer.data)
            except ValidationError as e:
                return HttpResponse(e, status=400)
        return JsonResponse({'message': 'error'}, status=400)


class ArticleDeleteView(APIView):
    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        article = Article.objects.get(id=pk)
        response = {"id": pk}
        article.delete()
        return HttpResponse(response, status=400)
