from datetime import datetime, timezone

import pytest

from main.models import Arch, Repo
from packages.models import Package, Signoff, SignoffSpecification


@pytest.fixture
def testing_package(db, arches, repos):
    repo = Repo.objects.get(name='Core-Testing')
    arch = Arch.objects.get(name='x86_64')
    now = datetime.now(tz=timezone.utc)
    package = Package.objects.create(arch=arch, repo=repo, pkgname='systemd',
                                     pkgbase='systemd', pkgver='0.1',
                                     pkgrel='1', pkgdesc='System and service manager',
                                     compressed_size=10, installed_size=20,
                                     last_update=now, created=now)
    yield package
    package.delete()


def test_signoffs(client, developer_client):
    response = client.get('/packages/signoffs/')
    assert response.status_code == 200


def test_signoffs_json(client, developer_client):
    response = client.get('/packages/signoffs/json/')
    assert response.status_code == 200
    assert response.json()['signoff_groups'] == []


def signoff_url(package, revoke=False):
    url = f'/packages/{package.repo.name.lower()}/{package.arch.name}/{package.pkgname}/signoff/'
    return url + 'revoke/' if revoke else url


HEADERS = {'X-Requested-With': 'XMLHttpRequest'}

def test_signoff_package(developer_client, developer, testing_package):
    response = developer_client.get(signoff_url(testing_package))
    assert response.status_code == 302
    assert response.url == '/packages/signoffs/'

    signoff = Signoff.objects.get(user=developer)
    assert signoff.pkgbase == testing_package.pkgbase
    assert signoff.revoked is None


def test_signoff_package_ajax(developer_client, testing_package):
    response = developer_client.get(signoff_url(testing_package), headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data['created'] is True
    assert data['revoked'] is False
    assert data['approved'] is False
    assert data['user'] == 'joeuser'

    # signing off twice does not create a second signoff
    response = developer_client.get(signoff_url(testing_package), headers=HEADERS)
    assert response.json()['created'] is False
    assert Signoff.objects.count() == 1


def test_signoff_revoke(developer_client, developer, testing_package):
    developer_client.get(signoff_url(testing_package))
    response = developer_client.get(signoff_url(testing_package, revoke=True), headers=HEADERS)
    assert response.status_code == 200
    assert response.json()['revoked'] is True
    assert Signoff.objects.get(user=developer).revoked is not None


def test_signoff_revoke_without_signoff(developer_client, testing_package):
    response = developer_client.get(signoff_url(testing_package, revoke=True))
    assert response.status_code == 404


def test_signoff_non_testing_package(developer_client, package):
    response = developer_client.get('/packages/core/x86_64/linux/signoff/')
    assert response.status_code == 404
    assert Signoff.objects.count() == 0


def test_signoff_anonymous(client, testing_package):
    response = client.get(signoff_url(testing_package))
    assert response.status_code == 302
    assert '/login/' in response.url
    assert Signoff.objects.count() == 0


@pytest.mark.parametrize(('enabled', 'known_bad'), [(False, False), (True, True)])
def test_signoff_not_accepted(developer_client, developer, testing_package, enabled, known_bad):
    SignoffSpecification.objects.create(
        pkgbase=testing_package.pkgbase, pkgver=testing_package.pkgver,
        pkgrel=testing_package.pkgrel, epoch=testing_package.epoch,
        arch=testing_package.arch, repo=testing_package.repo,
        user=developer, enabled=enabled, known_bad=known_bad)
    response = developer_client.get(signoff_url(testing_package))
    assert response.status_code == 403
    assert Signoff.objects.count() == 0


def test_signoff_approved_sends_mail(developer_client, developer, testing_package, mailoutbox):
    testing_package.packager = developer
    testing_package.save()
    SignoffSpecification.objects.create(
        pkgbase=testing_package.pkgbase, pkgver=testing_package.pkgver,
        pkgrel=testing_package.pkgrel, epoch=testing_package.epoch,
        arch=testing_package.arch, repo=testing_package.repo,
        user=developer, required=1)

    response = developer_client.get(signoff_url(testing_package), headers=HEADERS)
    assert response.json()['approved'] is True
    assert len(mailoutbox) == 1
    assert mailoutbox[0].to == [developer.email]
    assert 'approved' in mailoutbox[0].subject
