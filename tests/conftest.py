from pydoc import cli
import pytest
import string
from datetime import datetime, timedelta
import random
from cake_bake_app.models import EmployeesModel, CakePreferencesModel
from fastapi.testclient import TestClient
from cake_bake_app.app import app
from cake_bake_app.db import create_database_if_not_exists

create_database_if_not_exists()

client = TestClient(app)

letters = list(string.ascii_letters)
latest_birthday = datetime(2000, 3, 10, 00, 00, 00)
first_names = ["Joe", "Jane", "Vish", "Doe", "Dane", "Mish"]
last_names = ["".join(random.choices(letters, k=10)) for _ in range(len(first_names))]

# creating Employees
time_delta_days = 18 * 365  # 18 years in days
employees_models = []
for f, l in zip(first_names, last_names):
    dob = latest_birthday - timedelta(days=random.randrange(time_delta_days))
    _jsn = {"name": f"{f} {l}", "date_of_birth": dob.strftime("%Y-%m-%dT%H:%M:%S")}
    employees_models.append(_jsn)

# Creating Cake Preferences
food_intolerences = ["gluten", "milk", "egg", "soy", "nuts", "chocolate"]
cake_prefs = ["chocolate", "red velvet", "sponge", "tiramisu", "sticky toffee"]
cake_prefs_models = []
for emp in employees_models:
    _jsn = {
        "name": emp["name"],
        "food_intolerence": ", ".join(random.choices(food_intolerences, k=5)),
        "cake_preference": ", ".join(random.choices(cake_prefs, k=5)),
    }
    cake_prefs_models.append(_jsn)


@pytest.fixture
def employees():
    return employees_models


@pytest.fixture
def cake_preferences():
    return cake_prefs_models


@pytest.fixture
def test_client():
    return client
