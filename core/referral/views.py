from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django_tables2 import RequestConfig

from referral.forms import PresentForm, CreatePresentForm
from referral.models import Present
from referral.tables import PresentTable


@login_required()
@permission_required("referral.view_present", raise_exception=True)
def present_list_view(request: HttpRequest):
    table = PresentTable(Present.objects.all())
    RequestConfig(request, paginate={"per_page": 25}).configure(table)

    context = {
        "table": table,
        "header": "Список подарков",
        "breadcrumb_item1": "Меню администратора",
        "breadcrumb_item2": "Подарки",
        "disable_export": True,
        "disable_create": False,
        "create_url": reverse("cabinet:present_create_view"),
    }

    return render(request, "cabinet/layout/list.html", context)


@login_required()
@permission_required("referral.change_present", raise_exception=True)
def present_detail_view(request: HttpRequest, pk: int):
    present = get_object_or_404(Present, pk=pk)

    if request.method == "POST":
        if "delete" in request.POST:
            present.delete()
            return redirect("cabinet:present_list_view")

        form = PresentForm(request.POST, instance=present)
        if form.is_valid():
            form.save()
    else:
        form = PresentForm(instance=present)

    context = {"form": form}

    return render(request, "cabinet/layout/detail.html", context)


@login_required()
@permission_required("referral.add_present", raise_exception=True)
def present_create_view(request: HttpRequest):
    form = CreatePresentForm()

    if request.method == "POST":
        form = CreatePresentForm(request.POST)
        if form.is_valid():
            present = form.save()
            messages.success(request, "Подарок успешно добавлен!")
            return redirect(present.get_absolute_url())

    context = {
        "form": form,
        "header": form.layout_header,
        "breadcrumb_item2": form.layout_header,
    }

    return render(request, "cabinet/layout/detail.html", context)
