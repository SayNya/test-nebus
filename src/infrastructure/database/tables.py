from typing import TypeVar

from sqlalchemy import ForeignKey, Integer, MetaData, String, Float, Table, Column
from sqlalchemy.orm import declarative_base, mapped_column, Mapped, relationship

from src.infrastructure.errors import BadRequestError
from werkzeug.security import generate_password_hash, check_password_hash

__all__ = (
    "Base",
    "UserTable",
    "BuildingTable",
    "organization_activity",
    "OrganizationTable",
    "PhoneNumberTable",
    "ActivityTable",
    "ConcreteTable",
    "APIKeyTable",
    "user_organization",
)


meta = MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_`%(constraint_name)s`",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }
)


class _Base:
    id: Mapped[int] = mapped_column(Integer, primary_key=True)


Base = declarative_base(cls=_Base, metadata=meta)

ConcreteTable = TypeVar("ConcreteTable", bound=Base)


organization_activity = Table(
    "organization_activity",
    Base.metadata,
    Column("organization_id", ForeignKey("organization.id"), primary_key=True),
    Column("activity_id", ForeignKey("activity.id"), primary_key=True),
)

user_organization = Table(
    "user_organization",
    Base.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("organization_id", ForeignKey("organization.id"), primary_key=True),
)


class UserTable(Base):
    __tablename__ = "user"

    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    api_keys: Mapped[list["APIKeyTable"]] = relationship(back_populates="user")
    organizations: Mapped[list["OrganizationTable"]] = relationship(
        secondary=user_organization, back_populates="users"
    )

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


class APIKeyTable(Base):
    __tablename__ = "api_key"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    key: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)

    user: Mapped["UserTable"] = relationship(back_populates="api_keys")


class BuildingTable(Base):
    __tablename__ = "building"

    address: Mapped[str] = mapped_column(String(255), nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)

    organizations: Mapped[list["OrganizationTable"]] = relationship(
        back_populates="building"
    )


class ActivityTable(Base):
    __tablename__ = "activity"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("activity.id"), nullable=True
    )

    parent: Mapped["ActivityTable"] = relationship(
        remote_side="ActivityTable.id", back_populates="children"
    )
    children: Mapped[list["ActivityTable"]] = relationship(back_populates="parent")

    organizations: Mapped[list["OrganizationTable"]] = relationship(
        secondary=organization_activity, back_populates="activities"
    )

    def get_nesting_level(self) -> int:
        level = 0
        current = self
        while current.parent is not None:
            level += 1
            current = current.parent
        return level

    def validate_nesting_level(self):
        nesting_level = self.get_nesting_level()
        if nesting_level > 3:
            raise BadRequestError(
                message=f"Nesting level cannot exceed 3. Current level: {nesting_level}"
            )


class OrganizationTable(Base):
    __tablename__ = "organization"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    building_id: Mapped[int] = mapped_column(ForeignKey("building.id"), nullable=False)

    building: Mapped["BuildingTable"] = relationship(back_populates="organizations")
    phone_numbers: Mapped[list["PhoneNumberTable"]] = relationship(
        back_populates="organization"
    )
    activities: Mapped[list["ActivityTable"]] = relationship(
        secondary=organization_activity, back_populates="organizations"
    )
    users: Mapped[list["UserTable"]] = relationship(
        secondary=user_organization, back_populates="organizations"
    )


class PhoneNumberTable(Base):
    __tablename__ = "phone_number"

    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organization.id"), nullable=False
    )
    phone_number: Mapped[str] = mapped_column(String(20), nullable=False)

    organization: Mapped["OrganizationTable"] = relationship(
        back_populates="phone_numbers"
    )
