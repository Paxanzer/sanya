from django.urls import path, include
from .import views
# добавлено для работы с медиа файлами
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books-list'),
    path('books/<int:pk>/', views.BookDetailView.as_view(),
         name='book-detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors-list'),
    path('authors/<int:pk>/', views.AuthorDetailView.as_view(),
         name='authors-detail'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(),
         name='my-borrowed'),
    path('edit_authors/', views.edit_authors, name='edit_authors'),
    path('edit_authors/<int:id>', views.edit_authors, name='edit_authors1'),
    path('authors_add/', views.add_author, name='authors_add'),
    path('delete/<int:id>/', views.delete, name='delete'),
    path('edit_author/<int:id>/', views.edit_author, name='edit_author')

]

# добавлено для работы с медиа файлами локально
if settings.DEBUG:
 urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# добавлено для регистрации входа пользователей
urlpatterns += [
 path('accounts/', include('django.contrib.auth.urls')),
]
