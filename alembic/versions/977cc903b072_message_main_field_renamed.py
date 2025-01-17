"""Message main field renamed

Revision ID: 977cc903b072
Revises: ecc4097ed7e4
Create Date: 2024-10-20 16:59:26.845404

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '977cc903b072'
down_revision: Union[str, None] = 'ecc4097ed7e4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('messages', sa.Column('content', sa.String(), nullable=False))
    op.drop_column('messages', 'text')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('messages', sa.Column('text', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_column('messages', 'content')
    # ### end Alembic commands ###
