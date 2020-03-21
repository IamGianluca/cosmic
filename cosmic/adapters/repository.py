from abc import ABC, abstractmethod
from typing import List

from cosmic.domain.model import Batch


class AbstractRepository(ABC):
    @abstractmethod
    def add(self, batch: Batch):
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def get(self, reference: str) -> Batch:
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def list(self) -> List[Batch]:
        raise NotImplementedError  # pragma: no cover


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, batch: Batch):
        self.session.add(batch)

    def get(self, reference: str) -> Batch:
        return self.session.query(Batch).filter_by(reference=reference).one()

    def list(self) -> List[Batch]:
        return self.session.query(Batch).all()


class FakeRepository(AbstractRepository):
    def __init__(self, batches: List[Batch]):
        self._batches = set(batches)

    def add(self, batch: Batch):
        self._batches.add(batch)

    def get(self, reference: str) -> Batch:
        return next(b for b in self._batches if b.reference == reference)

    def list(self) -> List[Batch]:
        return list(self._batches)
