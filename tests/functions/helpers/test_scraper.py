from app.server.helpers.titler import get_title

text = "Things You Can Do With CSS Today — Smashing Magazine"
good_link = "https://www.smashingmagazine.com/2021/02/things-you-can-do-with-css-today/"
bad_link = "https://www.gmagazine.com/2021/02/things-you-can-do-with-css-today/"

def test_titler_success():
    res = get_title(good_link)
    assert res["title"] == text
    assert res["status"] == 200
    
def test_titler_fail():
    res = get_title(bad_link)
    assert not res