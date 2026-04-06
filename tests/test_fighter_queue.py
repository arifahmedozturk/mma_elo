import pytest
from FighterQueue.FighterQueue import FighterQueue


@pytest.fixture
def queue():
    return FighterQueue()


def test_pop_empty_returns_none(queue):
    assert queue.pop() is None


def test_insert_and_pop(queue):
    queue.insert("https://en.wikipedia.org/wiki/Jon_Jones")
    assert queue.pop() == "https://en.wikipedia.org/wiki/Jon_Jones"


def test_pop_moves_to_expanded(queue):
    url = "https://en.wikipedia.org/wiki/Jon_Jones"
    queue.insert(url)
    queue.pop()
    # Should not be re-insertable after popping
    queue.insert(url)
    assert queue.pop() is None


def test_duplicate_insert_ignored(queue):
    url = "https://en.wikipedia.org/wiki/Jon_Jones"
    queue.insert(url)
    queue.insert(url)
    queue.pop()
    assert queue.pop() is None


def test_multiple_fighters(queue):
    urls = [
        "https://en.wikipedia.org/wiki/Jon_Jones",
        "https://en.wikipedia.org/wiki/Khabib_Nurmagomedov",
        "https://en.wikipedia.org/wiki/Israel_Adesanya",
    ]
    for url in urls:
        queue.insert(url)

    popped = set()
    while True:
        url = queue.pop()
        if url is None:
            break
        popped.add(url)

    assert popped == set(urls)
