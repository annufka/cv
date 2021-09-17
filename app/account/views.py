from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import CreateView

from app.account.forms import SchemeForm, RowFormSet, LoginForm
from app.account.models import Schema, DataSet, ColumnSchema
from app.account.tasks import generate_csv


# немного не ясен первый пункт тестового, поэтому сделала так, чтобы мог зайти любой человек под любым логином и паролем, иначе эта часть комментируется и в urls раскомментируется строчка, а другая убирается
def login(request):
    form = LoginForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        user = authenticate(username=cd['username'], password=cd['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
            else:
                user = User.objects.create_user(username=cd['username'], password=cd['password'])
                login(request, user)
    else:
        form = LoginForm()
        return render(request, 'registration/login.html', {'form': form})
    schemas = Schema.objects.all().order_by('pk')
    return render(request, 'registration/schemas.html', {'schemas': schemas})


@login_required
def schemas(request):
    schemas = Schema.objects.all().order_by('pk')
    context = {'schemas': schemas}
    return render(request, 'registration/schemas.html', context)


@login_required
def scheme(request, scheme_id):
    scheme = get_object_or_404(Schema, pk=scheme_id)
    context = {'scheme': scheme}
    return render(request, 'registration/schema.html', context)


@login_required
def delete_scheme(request, scheme_id):
    # надо было автора схемы добавить в модель, а то так любой человек любую схему отредактирует и удалит. Если останется время и не забуду, то сделаю
    scheme = get_object_or_404(Schema, pk=scheme_id)
    scheme.delete()
    schemas = Schema.objects.all().order_by('pk')
    context = {'schemas': schemas}
    return render(request, 'registration/schemas.html', context)


# def create_scheme(request):
#     if request.method == "POST":
#         form = SchemeForm(request.POST)
#         if form.is_valid():
#             scheme = form.save(commit=False)
#             scheme.save()
#             return render(request, 'registration/schema.html',  {'scheme': scheme})
#     else:
#         form = SchemeForm()
#     return render(request, 'registration/create.html', {'form': form})
#
# def create_scheme_row(request, name):
#     scheme = Schema.objects.get(name=name)
#     if request.method == "POST":
#         form = RowFormSet(request.POST, instance=scheme)
#         if form.is_valid():
#             scheme = form.save(commit=False)
#             scheme.save()
#             return render(request, 'registration/schema.html',  {'scheme': scheme})
#     else:
#         form = RowFormSet(instance=scheme)
#     return render(request, 'registration/create.html', {"formset": form})

class FormsetMixin(object):
    object = None

    def get(self, request, *args, **kwargs):
        if getattr(self, 'is_update_view', False):
            self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset_class = self.get_formset_class()
        formset = self.get_formset(formset_class)
        return self.render_to_response(self.get_context_data(form=form, formset=formset))

    def post(self, request, *args, **kwargs):
        if getattr(self, 'is_update_view', False):
            self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset_class = self.get_formset_class()
        formset = self.get_formset(formset_class)
        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)

    def get_formset_class(self):
        return self.formset_class

    def get_formset(self, formset_class):
        return formset_class(**self.get_formset_kwargs())

    def get_formset_kwargs(self):
        kwargs = {
            'instance': self.object
        }
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def form_valid(self, form, formset):
        self.object = form.save()
        formset.instance = self.object
        formset.save()
        return redirect(reverse("sets"))

    def form_invalid(self, form, formset):
        return self.render_to_response(self.get_context_data(form=form, formset=formset))

class SchemeAndRow(FormsetMixin, CreateView):
    template_name = 'registration/create.html'
    model = Schema
    form_class = SchemeForm
    formset_class = RowFormSet

@login_required
def get_sets(request):
    sets = DataSet.objects.all()
    context = {'sets': sets}
    return render(request, 'registration/sets.html', context)


def generate_sets(request):
    context = {}
    generate_number = request.POST.get('generate_number')
    sets = DataSet.objects.all()
    for set in sets:
        generate_csv.delay(set.pk, generate_number)
        set.path_to_file = set.schema.name + '.csv'
        set.save()
    context = {'sets': sets}
    return render(request, 'registration/sets.html', context)

# class TaskView(View):
#     def get(self, request, task_id):
#         task = current_app.AsyncResult(task_id)
#         response_data = {'task_status': task.status, 'task_id': task.id}
#         if task.status == 'SUCCESS':
#             response_data['results'] = task.get()
#         return JsonResponse(response_data)
