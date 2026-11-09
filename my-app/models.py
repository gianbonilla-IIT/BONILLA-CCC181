from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Identity,
    Index,
    String,
    func,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class Room(db.Model):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    name: Mapped[str] = mapped_column(String(80))
    meeting_link: Mapped[str] = mapped_column(String(300))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    tickets: Mapped[list["Ticket"]] = relationship(back_populates="room")

    __table_args__ = (
        CheckConstraint("meeting_link ~ '^https?://'", name="ck_rooms_meeting_link"),
    )


class Service(db.Model):
    __tablename__ = "services"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    name: Mapped[str] = mapped_column(String(60), unique=True)
    code: Mapped[str] = mapped_column(String(4), unique=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True, server_default=text("true"))

    tickets: Mapped[list["Ticket"]] = relationship(back_populates="service")

    __table_args__ = (
        CheckConstraint("code ~ '^[A-Z]{2,4}$'", name="ck_services_code"),
    )


class Ticket(db.Model):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id", ondelete="RESTRICT"))
    service_id: Mapped[int] = mapped_column(ForeignKey("services.id", ondelete="RESTRICT"))
    group_name: Mapped[str] = mapped_column(String(60))
    topic: Mapped[str] = mapped_column(String(150))
    status: Mapped[str] = mapped_column(String(20), default="waiting", server_default="waiting")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    room: Mapped["Room"] = relationship(back_populates="tickets")
    service: Mapped["Service"] = relationship(back_populates="tickets")

    __table_args__ = (
        CheckConstraint(
            "status IN ('waiting', 'called', 'served', 'no-show', 'left')",
            name="ck_tickets_status",
        ),
        CheckConstraint("length(trim(group_name)) > 0", name="ck_tickets_group_name"),
        CheckConstraint("length(trim(topic)) > 0", name="ck_tickets_topic"),
        # One active ticket per group name in a room (see docs/week4/schema.md)
        Index(
            "ux_tickets_active_group_name",
            "room_id",
            text("lower(group_name)"),
            unique=True,
            postgresql_where=text("status IN ('waiting', 'called')"),
        ),
        # At most one ticket is being called at a time in a room (added by migration 2)
        Index(
            "ux_tickets_one_called_per_room",
            "room_id",
            unique=True,
            postgresql_where=text("status = 'called'"),
        ),
    )