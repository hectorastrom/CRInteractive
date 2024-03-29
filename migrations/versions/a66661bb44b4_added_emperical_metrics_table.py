"""added emperical metrics table

Revision ID: a66661bb44b4
Revises: f3977f0a625c
Create Date: 2021-11-14 12:41:39.084706

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a66661bb44b4'
down_revision = 'f3977f0a625c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('emp_metrics',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tag', sa.String(length=5), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('desc', sa.Text(), nullable=True),
    sa.Column('team', sa.String(length=20), nullable=False),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('for_cox', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('emp_metrics')
    # ### end Alembic commands ###
