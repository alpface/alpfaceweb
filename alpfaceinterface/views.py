from django.shortcuts import render
import json
from django.http import HttpResponse, HttpResponseRedirect
from alpfaceinterface.main import main


# Create your views here.

def answer_test(request):
    return render(request, 'alpfaceinterface/question1.html')


def answer_options(request):

    question = request.POST['question_text']
    answeroption1 = request.POST['answeroptions1']
    answeroption2 = request.POST['answeroptions2']
    answeroption3 = request.POST['answeroptions3']
    answeroption4 = request.POST['answeroptions4']
    # str_options = ",".join(answeroptions)
    main('{question}\n\n{op1}\n\n{op2}\n\n{op3}\n\n{op4}'.format(
        question=question,
        op1=answeroption1,
        op2=answeroption2,
        op3=answeroption3,
        op4=answeroption4
    ))
    # resp = {'errorCode': 100, 'detail': 'Get success', 'question': question, 'answeroptions': answeroptions}
    resp = {}
    #return HttpResponse(json.dumps(resp), content_type='application/json')
    return HttpResponseRedirect('/alpfaceinterface/answertest/')

