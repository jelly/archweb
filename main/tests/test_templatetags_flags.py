import pytest

from main.templatetags.flags import country_flag
from conftest import create_checklocation


@pytest.mark.django_db(transaction=True)
def test_country_flag():
    checkloc = create_checklocation()
    flag = country_flag(checkloc.country)
    assert checkloc.country.name in flag
    assert checkloc.country.code.lower() in flag
    assert country_flag(None) == ''
