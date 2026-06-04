"""Модель заявки на обслуживание"""

from app.models.base import (
    BaseModel,
    ForeignKey,
    Mapped,
    String,
    Text,
    mapped_column,
    relationship,
)
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.contract import Contract


class Request(BaseModel):
    """Заявка на обслуживание/ремонт от арендатора"""

    __tablename__ = "requests"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    contract_id: Mapped[int] = mapped_column(
        ForeignKey("contracts.id"), index=True, nullable=False
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False, default="Заявка")
    message: Mapped[str] = mapped_column(Text(), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False)

    contract: Mapped["Contract"] = relationship("Contract", back_populates="requests")
