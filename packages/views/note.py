import re

from django import forms
from django.contrib.auth.decorators import permission_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.template import loader
from django.utils.timezone import now
from django.views.decorators.cache import cache_page, never_cache

from main.models import Package

from ..models import PackageNote


class NoteForm(forms.Form):
    note = forms.CharField(label='Note to users',
                           widget=forms.Textarea)


@permission_required('main.change_package')
def note(request, name, repo, arch):
    pkg = get_object_or_404(Package.objects.normal(),
                            pkgname=name, repo__name__iexact=repo, arch__name=arch)
    # find all packages from (hopefully) the same PKGBUILD
    pkgs = Package.objects.normal().filter(
        pkgbase=pkg.pkgbase, flag_date__isnull=True,
        repo__testing=pkg.repo.testing,
        repo__staging=pkg.repo.staging).order_by(
        'pkgname', 'repo__name', 'arch__name')

    if request.POST:
        form = NoteForm(request.POST)
        if form.is_valid():
            # save the package list for later use
            note_pkgs = list(pkgs)

            # find a common version if there is one available to store
            versions = {(pkg.pkgver, pkg.pkgrel, pkg.epoch) for pkg in note_pkgs}
            if len(versions) == 1:
                version = versions.pop()
            else:
                version = ('', '', 0)

            note = form.cleaned_data['note']

            @transaction.atomic
            def perform_updates():
                current_time = now()
                # store our package note
                package_note = PackageNote(created=current_time,
                                           note=note,
                                           pkgbase=pkg.pkgbase,
                                           repo=pkg.repo, pkgver=version[0], pkgrel=version[1],
                                           epoch=version[2], num_packages=len(note_pkgs))
                package_note.save()

            perform_updates()

            return redirect('package-note-confirmed', name=name, repo=repo, arch=arch)
    else:
        form = NoteForm()

    context = {
        'package': pkg,
        'packages': pkgs,
        'form': form
    }
    return render(request, 'packages/note.html', context)


def note_confirmed(request, name, repo, arch):
    pkg = get_object_or_404(Package,
                            pkgname=name, repo__name__iexact=repo, arch__name=arch)
    pkgs = Package.objects.normal().filter(
        pkgbase=pkg.pkgbase, flag_date=pkg.flag_date,
        repo__testing=pkg.repo.testing,
        repo__staging=pkg.repo.staging).order_by(
        'pkgname', 'repo__name', 'arch__name')

    context = {'package': pkg, 'packages': pkgs}

    return render(request, 'packages/note_confirmed.html', context)

# vim: set ts=4 sw=4 et:
