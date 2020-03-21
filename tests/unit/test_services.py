from cosmic.adapters import repository
from cosmic.domain import model
from cosmic.service_layer import services


class FakeSession:
    committed = False

    def commit(self):
        self.committed = True


def test_returns_allocation():
    # given
    line = model.OrderLine("o1", "COMPLICATED-LAMP", 10)
    batch = model.Batch("b1", "COMPLICATED-LAMP", 100, eta=None)
    repo = repository.FakeRepository([batch])

    # when
    result = services.allocate(line, repo, FakeSession())

    # then
    assert result == "b1"


def test_commits():
    # given
    line = model.OrderLine("o1", "OMINOUS-MIRROR", 10)
    batch = model.Batch("b1", "OMINOUS-MIRROR", 100, eta=None)
    repo = repository.FakeRepository([batch])
    session = FakeSession()

    # when
    services.allocate(line, repo, session)

    # then
    assert session.committed == True
