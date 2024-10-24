"""Added tg_id to User model

Revision ID: 94be7bd1ea2b
Revises: 7fba1d7683c3
Create Date: 2024-10-20 18:34:40.889681

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '94be7bd1ea2b'
down_revision: Union[str, None] = '7fba1d7683c3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('tg_id', sa.Integer(), nullable=True))
    op.create_unique_constraint(None, 'users', ['tg_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_column('users', 'tg_id')
    # ### end Alembic commands ###
