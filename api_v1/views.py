from django.shortcuts import render

# Create your views here.
import json
from django.http import HttpResponseNotAllowed, HttpResponseBadRequest, JsonResponse


def validate_nums(data):
    a = data.get("A")
    b = data.get("B")
    if a is not None and b is not None and isinstance(a, int) and isinstance(b, int):
        return True
    return False


def add(request, *args, **kwargs):
    if request.method != "POST":
        return HttpResponseNotAllowed(permitted_methods=["POST"])
    if request.body:
        nums = json.loads(request.body)
        if not validate_nums(nums):
            response = {"error": "Данные не являются числами!"}
            return HttpResponseBadRequest(json.dumps(response))
        response = {'answer': nums['A'] + nums['B']}
        return JsonResponse(response)


def subtract(request, *args, **kwargs):
    if request.method != "POST":
        return HttpResponseNotAllowed(permitted_methods=["POST"])
    if request.body:
        nums = json.loads(request.body)
        if not validate_nums(nums):
            response = {"error": "Данные не являются числами!"}
            return HttpResponseBadRequest(json.dumps(response))
        response = {'answer': nums['A'] - nums['B']}
        return JsonResponse(response)


def multiply(request, *args, **kwargs):
    if request.method != "POST":
        return HttpResponseNotAllowed(permitted_methods=["POST"])
    if request.body:
        nums = json.loads(request.body)
        if not validate_nums(nums):
            response = {"error": "Данные не являются числами!"}
            return HttpResponseBadRequest(json.dumps(response))
        response = {'answer': nums['A'] * nums['B']}
        return JsonResponse(response)


def divide(request, *args, **kwargs):
    if request.method != "POST":
        return HttpResponseNotAllowed(permitted_methods=["POST"])
    if request.body:
        nums = json.loads(request.body)
        if not validate_nums(nums):
            response = {"error": "Данные не являются числами!"}
            return HttpResponseBadRequest(json.dumps(response))
        if nums.get("B") == 0:
            response = {"error": "Деление на ноль"}
            return HttpResponseBadRequest(json.dumps(response))
        response = {'answer': nums['A'] / nums['B']}
        return JsonResponse(response)
