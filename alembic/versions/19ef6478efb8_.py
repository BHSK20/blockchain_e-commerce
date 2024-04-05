"""empty message

Revision ID: 19ef6478efb8
Revises: 02918756190b
Create Date: 2024-04-05 23:25:07.011535

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '19ef6478efb8'
down_revision: Union[str, None] = '02918756190b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # add user column to table Orders
    op.add_column('Orders', sa.Column('user', sa.String(), nullable=True))


def downgrade() -> None:
    # drop user column from table Orders
    op.drop_column('Orders', 'user')
