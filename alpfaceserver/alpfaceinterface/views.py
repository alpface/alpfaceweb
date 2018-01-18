from django.shortcuts import render
import json
from django.http import HttpResponse
from alpfaceserver.alpfaceinterface.main import search


# Create your views here.

def answer_test(request):
    return render(request, 'alpfaceinterface/question1.html')


def answer_options(request):

    question = request.POST['question_text']
    answeroptions = request.POST.getlist('answeroptions')

    search(question+answeroptions)

    resp = {'errorCode': 100, 'detail': 'Get success', 'question': question, 'answeroptions': answeroptions}
    return HttpResponse(json.dumps(resp), content_type='application/json')

