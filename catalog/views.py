from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import generic

from catalog.models import Book, BookIstance, Author, Genre


def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookIstance.objects.all().count()
    num_genres = Genre.objects.count()
    num_instances_available = BookIstance.objects.filter(status__exact='a').count()
    num_authors = BookIstance.objects.count()
    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = 1
    return render(request, 'index.html', context={'num_books': num_books, 'num_instances': num_instances,
                                                  'num_instances_available': num_instances_available,
                                                  'num_authors': num_authors,
                                                  'num_genres': num_genres, "num_visits": num_visits})


class BookListView(generic.ListView):
    model = Book
    paginate_by = 10


class BookDetailView(generic.DetailView):
    model = Book


class AuthorListView(generic.ListView):
    model = Author


class AuthorDetailView(generic.DetailView):
    model = Author

    def get_context_data(self, **kwargs):
        ctx = super(AuthorDetailView, self).get_context_data(**kwargs)
        ctx['book'] = Book.objects.all()
        return ctx


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookIstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookIstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')
