"""Added 5k

Revision ID: 543d4a576dbd
Revises: ef5be88b8c83
Create Date: 2021-09-09 17:57:32.534329

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '543d4a576dbd'
down_revision = 'ef5be88b8c83'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('fivek',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('seconds', sa.Float(), nullable=False),
    sa.Column('date_completed', sa.Date(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('fivek')
    # ### end Alembic commands ###
