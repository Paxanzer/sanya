from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.views.generic import ListView, DetailView
from catalog.models import Book, BookInstance, Author, Gun
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

def index(request):
 text_head = 'На нашем сайте вы можете ознакомиться с нашими экспонатами.'
 # Данные о книгах и их количестве
 guns = Gun.objects.all()
 num_books = Book.objects.all().count()
 # Данные об экземплярах книг в БД
 num_instances = BookInstance.objects.all().count()
 # Доступные книги (статус = 'На складе')
 num_instances_available = BookInstance.objects.filter(
 status__exact=2).count()
 # Данные об авторах книг
 authors = Author.objects
 num_authors = Author.objects.count()
 # Количество посещений этого view, подсчитанное в переменной session
 num_visits = request.session.get('num_visits', 0)
 request.session['num_visits'] = num_visits + 1
 # Словарь для передачи данных в шаблон index.html
 context = {'text_head': text_head,
 'guns': guns, 'num_books': num_books,
 'num_instances': num_instances,
 'num_instances_available': num_instances_available,
 'authors': authors, 'num_authors': num_authors,
 'num_visits': num_visits
 }
 # передача словаря context с данными в шаблон
 return render(request, 'catalog/index.html', context)


class BookListView(ListView):
    model = Gun
    context_object_name = 'gun'
    paginate_by = 10

class BookDetailView(DetailView):
    model = Gun
    context_object_name = 'gun'


class AuthorListView(ListView):
    model = Gun
    paginate_by = 4


class AuthorDetailView(DetailView):
    model = Author


def about(request):
    text_head = 'О нас'
    name = 'ООО "Музей оружия Курск"'
    rab1 = 'Сбор, сохранение, интерпретация и демонстрация предметов, имеющих художественное, культурное или научное значение для изучения и образования общественности. С точки зрения посетителя или сообщества, эта цель также может зависеть от точки зрения человека.'
    rab2 = 'Распознавание объектов дорожной инфраструктуры'
    rab3 = 'Создание графических АРТ-объектов на основе' \
    ' систем искусственного интеллекта'
    rab4 = 'Создание цифровых интерактивных книг, учебных пособий' \
    ' автоматизированных обучающих систем'
    context = {'text_head': text_head, 'name': name,
    'rab1': rab1, 'rab2': rab2,
    'rab3': rab3, 'rab4': rab4}
    # передача словаря context с данными в шаблон
    return render(request, 'catalog/about.html', context)

def contact(request):
    text_head = 'Контакты'
    name = 'ООО "Музей оружия Курск"'
    address = 'Курск, ул. Гагарина, д. 27 '
    tel = '+7 (920) 268 22-10'
    email = 'teatrekursk@mail.ru'
    # Словарь для передачи данных в шаблон index.html
    context = {'text_head': text_head,
    'name': name, 'address': address,
    'tel': tel,
    'email': email}
    # передача словаря context с данными в шаблон
    return render(request, 'catalog/contact.html', context)


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
 # Универсальный класс представления списка книг,
 # находящихся в заказе у текущего пользователя
 model = BookInstance
 template_name = 'catalog/bookinstance_list_borrowed_user.html'
 paginate_by = 10

 def get_queryset(self):
    return BookInstance.objects.filter(
        borrower=self.request.user).filter(
        status__exact='2').order_by('due_back')


# вызов страницы для редактирования авторов
def edit_authors(request):
 gun = Gun.objects.all()
 context = {'gun': gun}
 return render(request, "catalog/edit_authors.html", context)

def edit_author(request, id):
 gun = Gun.objects.get(id=id)
 # author = get_object_or_404(Author, pk=id)
 if request.method == "POST":
    instance = Gun.objects.get(pk=id)
    form = Form_edit_author(request.POST, request.FILES, instance=instance)
    if form.is_valid():
        form.save()

        return HttpResponseRedirect("/edit_authors/")
 else:
    form = Form_edit_author(instance=gun)
    content = {"form": form}
    return render(request, "catalog/edit_author.html", content)

# импорт для добавления автора
from .forms import Form_add_author, Form_edit_author
from django.urls import reverse
# Создание нового автора в БД
def add_author(request):
 if request.method == 'POST':
    form = Form_add_author(request.POST, request.FILES)
    if form.is_valid():
     #получить данные из формы
        title = form.cleaned_data.get("title")
        summary = form.cleaned_data.get("summary")
        photo = form.cleaned_data.get("photo")
        # создать объект для записи в БД
        obj = Gun.objects.create(
        title=title,
        summary=summary,
        photo=photo)
        # сохранить полученные данные
        obj.save()
    # загрузить страницу со списком автором
        return HttpResponseRedirect(reverse('edit_authors'))
 else:
    form = Form_add_author()
    context = {"form": form}
    return render(request, "catalog/authors_add.html", context)


# удаление авторов из БД
def delete(request, id):
 try:
    gun = Gun.objects.get(id=id)
    gun.delete()
    return HttpResponseRedirect("/edit_authors/")
 except:
    return HttpResponseNotFound("<h2>Эксонат не найден</h2>")
