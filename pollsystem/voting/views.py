# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponseRedirect
from django.urls import reverse
#from django.shortcuts import render
from django.shortcuts import get_list_or_404, get_object_or_404,render
# Create your views here.
from django.http import HttpResponse
from .models import Question,Choice
from django.http import Http404


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list, }
    return render(request, 'index.html', context)
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'detail.html', {'question': question})
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'results.html', {'question': question})
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=int(request.POST['choice']))
    except (KeyError, Choice.DoesNotExist):
        #display the question voting form
        return render(request, 'detail.html', {'question': question, 'error_message':"You didn't select a choice",})
    else:
        selected_choice.votes += 1
        selected_choice.save()
        #Always submit an HttpResponseRedirect after successfully dealing with POST data
        #This prevents the form being posted twice if a user hits the back button
        return HttpResponseRedirect(reverse('voting:results', args=(question.id,)))


