"""Message model relations fixed once again

Revision ID: 8c362bc4426b
Revises: c3ce17e20da9
Create Date: 2024-10-20 00:01:30.186467

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8c362bc4426b'
down_revision: Union[str, None] = 'c3ce17e20da9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'messages', 'users', ['sender_id'], ['id'])
    op.create_foreign_key(None, 'messages', 'users', ['receiver_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'messages', type_='foreignkey')
    op.drop_constraint(None, 'messages', type_='foreignkey')
    # ### end Alembic commands ###