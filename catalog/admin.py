from django.contrib import admin

from .models import Author, Book, Genre, Language, Publisher, Status, BookInstance, Gun

#admin.site.register(Author)
#admin.site.register(Book)
admin.site.register(Genre)
admin.site.register(Language)
admin.site.register(Publisher)
admin.site.register(Status)
admin.site.register(Gun)
#admin.site.register(BookInstance)

class AuthorAdmin(admin.ModelAdmin) :
    list_display = ('last_name', 'first_name', 'date_of_birth', 'photo')


admin.site.register(Author, AuthorAdmin)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin) :
    list_display = ('title', 'genre', 'language')


# Регистрируем класс BookInstanceAdmin для экземпляров книг
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
 list_display = ('book', 'status', 'borrower', 'due_back', 'id')
 list_filter = ('book', 'status')
 fieldsets = (('Экземпляр книги', {'fields': ('book', 'inv_nom')}),('Статус и окончание его действия', {'fields': ('status', 'due_back', 'borrower')}),)
