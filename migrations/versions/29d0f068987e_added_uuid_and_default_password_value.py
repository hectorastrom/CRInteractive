"""added uuid and default password value

Revision ID: 29d0f068987e
Revises: f948f5e693d9
Create Date: 2021-10-02 19:28:28.699762

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '29d0f068987e'
down_revision = 'f948f5e693d9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('uuid', sa.String(length=60), nullable=False))
    op.alter_column('user', 'password',
               existing_type=sa.VARCHAR(length=60),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'password',
               existing_type=sa.VARCHAR(length=60),
               nullable=False)
    op.drop_column('user', 'uuid')
    # ### end Alembic commands ###
