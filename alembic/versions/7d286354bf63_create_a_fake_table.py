"""create a fake table

Revision ID: 7d286354bf63
Revises: 
Create Date: 2023-03-28 15:51:21.603634

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7d286354bf63'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # op.create_table('fakeposttable',sa.Column('id',sa.Integer(), primary_key=True,nullable=False),
    #                 sa.Column('title',sa.String(),nullable=False))
    
    op.drop_column("post","likes")
    pass


def downgrade() -> None:
    # op.drop_table('fakeposttable')
    pass
