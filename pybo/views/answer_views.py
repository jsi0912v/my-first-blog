from django.shortcuts import redirect, render, get_object_or_404, resolve_url
from django.utils import timezone
from ..models import Answer, Question
from ..forms import AnswerForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.

@login_required(login_url='common:login')
def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.create_date=timezone.now()
            answer.question = question
            answer.save()
            print('{}#answer_{}'.format(resolve_url('pybo:detail', question_id=question.id), answer.id))
            return redirect('{}#answer_{}'.format(resolve_url('pybo:detail', question_id=question.id), answer.id))
    else:
        form = AnswerForm()
    context = { 'question': question, 'form': form }
    return render(request, 'pybo/question_detail.html', context )
    
    
    '''

    아래와 같이 변경하여 사용할 수 있다.
    
        from .models import Answer
        
        answer = Answer(question = question, content = request.POST.get('content'), create_date=timezone.now())
        answer.save()
    
    '''

@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '수정권한이 없습니다.')
        return redirect('pybo:detail', question_id=answer.question.id)
    
    if request.method == "POST":
        form = AnswerForm(request.POST, instance = answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.modify_date = timezone.now()
            answer.save()
            print('{}#answer_{}'.format(resolve_url('pybo:detail', question_id = answer.question.id), answer.id))
            return redirect( '{}#answer_{}'.format(resolve_url('pybo:detail', question_id = answer.question.id), answer.id) )
    else:
        form = AnswerForm(instance = answer) ## instance는 기본 입력 값을 전달.
    context = { 'answer': answer, 'form': form }
    return render(request, 'pybo/answer_form.html', context)

@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('pybo:detail', question_id=answer.question.id)
    
    answer.delete()
    return redirect( 'pybo:detail', question_id=answer.question.id)