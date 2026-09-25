
import pytest

from app.utils.preprocessing import extract_age


@pytest.mark.parametrize(
    "age_string, expected",
    [
        ("18 Years", 216),
        ("6 Months", 6),
        ("2 Weeks", 24 / 52.1775),
        ("7 Days", 84 / 365.2425),
        ("0 Years", 0),
        ("", None),
        (None, None),
        ("Unknown", None),
    ]
)
def test_extract_age(age_string, expected):
    result = extract_age(age_string)

    if expected is None:
        assert result is None
    else:
        assert result == pytest.approx(expected)