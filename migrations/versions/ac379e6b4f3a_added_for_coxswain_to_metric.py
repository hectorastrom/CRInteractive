"""added for coxswain to metric

Revision ID: ac379e6b4f3a
Revises: ae365edbe338
Create Date: 2021-10-11 12:02:27.735833

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ac379e6b4f3a'
down_revision = 'ae365edbe338'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('metric', sa.Column('for_coxswain', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('metric', 'for_coxswain')
    # ### end Alembic commands ###
