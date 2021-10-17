"""added default on to user

Revision ID: c03f4c8fa611
Revises: 1b092a35c3e0
Create Date: 2021-09-26 13:18:39.778448

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c03f4c8fa611'
down_revision = '1b092a35c3e0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('default_on', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'default_on')
    # ### end Alembic commands ###