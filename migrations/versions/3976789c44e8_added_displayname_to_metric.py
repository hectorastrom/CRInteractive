"""added displayname to metric

Revision ID: 3976789c44e8
Revises: 2ee4f4eb3478
Create Date: 2021-09-25 13:34:47.572567

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3976789c44e8'
down_revision = '2ee4f4eb3478'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('metric', sa.Column('metric_displayname', sa.String(length=50), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('metric', 'metric_displayname')
    # ### end Alembic commands ###
