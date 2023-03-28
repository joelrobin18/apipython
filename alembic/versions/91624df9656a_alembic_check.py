"""alembic check

Revision ID: 91624df9656a
Revises: 
Create Date: 2023-03-29 05:21:23.007959

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '91624df9656a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("votes",sa.Column("random check",sa.Integer()))
    pass


def downgrade() -> None:
    op.drop_column("votes","random check")
    pass
