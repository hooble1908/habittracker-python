from habits import choose_period

#correct spelling of period critical for further functions in application, therefore testing 
def test_choose_period_weekly(monkeypatch):
    """
    Parameters:
    monkeypatch : to mock user input to "w"
    to be honest - found no proper way to test wrong userinput because of while loop in function
    Returns:
    period is set to "weekly"
    """
    monkeypatch.setattr('builtins.input', lambda _: "w")
    result = choose_period()
    assert result == "weekly"


def test_choose_period_daily(monkeypatch):
    """
    Parameters:
    monkeypatch : to mock user input to "d"
    to be honest - found no proper way to test wrong userinput because of while loop in function
    Returns:
    period is set to "daily"
    """
    monkeypatch.setattr('builtins.input', lambda _: "d")
    result = choose_period()
    assert result == "daily"

   