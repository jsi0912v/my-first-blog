from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from .models import Answer, Question
from .forms import QuestionForm, AnswerForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.


def index(request):
    
    #페이지를 얻어옴
    page = request.GET.get('page', '1') 
    
    #조회
    question_list = Question.objects.order_by('-create_date')
    
    #페이지 처리
    paginator = Paginator(question_list, 10) #페이지당 10개씩 보여주기.
    page_obj = paginator.get_page(page)
    
    context = { "question_list" : page_obj }
    
    return render(request, 'pybo/question_list.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = { 'question' : question }
    
    return render(request, 'pybo/question_detail.html', context)

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
            return redirect('pybo:detail', question_id=question.id)
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
def question_create(request):
    
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.create_date = timezone.now()
            question.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = QuestionForm()
    context = { 'form' : form }
    return render(request, 'pybo/question_form.html', context)

@login_required(login_url='common:login')
def question_modify(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '수정권한이 없습니다.')
        return redirect('pybo:detail', question_id=question.id)
    
    if request.method == "POST":
        form = QuestionForm(request.POST, instance = question)
        if form.is_valid():
            question = form.save(commit=False)
            question.modify_date = timezone.now()
            question.save()
            return redirect( 'pybo:detail', question_id = question.id )
    else:
        form = QuestionForm(instance = question) ## instance는 기본 입력 값을 전달.
    context = { 'form': form }
    return render(request, 'pybo/question_form.html', context)

@login_required(login_url='common:login')
def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('pybo:detail', question_id=question.id)
    
    question.delete()
    return redirect( 'pybo:index')

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
            return redirect( 'pybo:detail', question_id = answer.question.id )
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