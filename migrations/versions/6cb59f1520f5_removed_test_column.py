"""removed test column

Revision ID: 6cb59f1520f5
Revises: 6459314a541b
Create Date: 2021-10-17 10:53:17.033911

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6cb59f1520f5'
down_revision = '6459314a541b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'test')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('test', sa.BOOLEAN(), nullable=True))
    # ### end Alembic commands ###
