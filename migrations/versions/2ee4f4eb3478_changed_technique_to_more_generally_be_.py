"""Changed technique to more generally be metric

Revision ID: 2ee4f4eb3478
Revises: a158db4aa4fd
Create Date: 2021-09-24 22:58:11.438587

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2ee4f4eb3478'
down_revision = 'a158db4aa4fd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('metric',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('metric_name', sa.String(length=50), nullable=False),
    sa.Column('coach_rating', sa.Integer(), nullable=True),
    sa.Column('coach_importance', sa.Integer(), nullable=True),
    sa.Column('user_rating', sa.Integer(), nullable=True),
    sa.Column('user_importance', sa.Integer(), nullable=True),
    sa.Column('view_allowed', sa.Boolean(), nullable=True),
    sa.Column('has_set', sa.Boolean(), nullable=True),
    sa.Column('note', sa.Text(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('technique')
    op.add_column('user', sa.Column('pinged', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'pinged')
    op.create_table('technique',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('coach_rating', sa.INTEGER(), nullable=True),
    sa.Column('user_rating', sa.INTEGER(), nullable=True),
    sa.Column('user_importance', sa.INTEGER(), nullable=True),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.Column('view_allowed', sa.BOOLEAN(), nullable=True),
    sa.Column('coach_importance', sa.INTEGER(), nullable=True),
    sa.Column('has_set', sa.BOOLEAN(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('metric')
    # ### end Alembic commands ###
