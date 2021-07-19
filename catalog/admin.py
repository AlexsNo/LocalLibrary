from django.contrib import admin

from catalog.models import Book, Genre, BookIstance, Author


class BookInline(admin.TabularInline):
    model = Book


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_died')
    fields = ('first_name','last_name',('date_of_birth','date_of_died'))
    inlines = [BookInline]


class BookInstanceInline(admin.TabularInline):
    model = BookIstance


class BookAdmin(admin.ModelAdmin):
    list_display = ('title','author','display_genre')
    inlines = [BookInstanceInline]

class GenreAdmin(admin.ModelAdmin):
    pass


class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book','status','due_back','id')
    list_filter = ('status','due_back')
    fieldsets = ((None,
                  {'fields': ('book', 'imprint', 'id')})
                 , ('Availability', {'fields': ('status', 'due_back')}))

admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(BookIstance, BookInstanceAdmin)
