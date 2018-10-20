import pytest

from mirrors.models import CheckLocation


@pytest.mark.django_db(transaction=True)
def create_checklocation(hostname='arch.org', source_ip='127.0.0.1', country='US'):
    return CheckLocation.objects.create(hostname=hostname,
                                        source_ip=source_ip,
                                        country=country)
