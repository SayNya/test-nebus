"""empty message

Revision ID: a60dea6eec1b
Revises: 49c6e8e54bcf
Create Date: 2025-02-04 07:02:36.253612

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a60dea6eec1b"
down_revision: Union[str, None] = "49c6e8e54bcf"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "user_organization",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("organization_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["organization_id"],
            ["organization.id"],
            name=op.f("fk_user_organization_organization_id_organization"),
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["user.id"], name=op.f("fk_user_organization_user_id_user")
        ),
        sa.PrimaryKeyConstraint(
            "user_id", "organization_id", name=op.f("pk_user_organization")
        ),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("user_organization")
    # ### end Alembic commands ###
