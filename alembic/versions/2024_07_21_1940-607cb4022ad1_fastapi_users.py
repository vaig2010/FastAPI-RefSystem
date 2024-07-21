"""fastapi-users

Revision ID: 607cb4022ad1
Revises: 3173242d17a2
Create Date: 2024-07-21 19:40:57.711126

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '607cb4022ad1'
down_revision: Union[str, None] = '3173242d17a2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('referral_codes')
    op.create_index(op.f('ix_users_code_id'), 'users', ['code_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_code_id'), table_name='users')
    op.create_table('referral_codes',
    sa.Column('code', sa.VARCHAR(), nullable=False),
    sa.Column('created_date', sa.DATETIME(), nullable=False),
    sa.Column('expiration_date', sa.DATETIME(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=False),
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('code')
    )
    # ### end Alembic commands ###
