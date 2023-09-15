from sqlalchemy import Column, DateTime, ForeignKey, Integer, PrimaryKeyConstraint, String, func
from sqlalchemy.orm import DeclarativeBase

from src.settings import settings


class Base(DeclarativeBase):
    def __repr__(self) -> str:
        return "<{}({})>".format(
            self.__class__.__name__,
            ', '.join(
                ["{}={}".format(k, repr(self.__dict__[k]))
                    for k in sorted(self.__dict__.keys())
                    if k[0] != '_']
            )
        )
