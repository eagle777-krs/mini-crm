from app.forms import RegisterForm, ClientForm, DealForm


def test_register_form_valid():
    form = RegisterForm(username="newuser", email="u@u.u", password="secret")
    assert form.validate() is True

def test_client_form_invalid_email():
    form = ClientForm(name="Test", email="wrong_email", phone_number="123")
    assert not form.validate()

def test_deal_form_empty():
    form = DealForm()
    assert not form.validate()