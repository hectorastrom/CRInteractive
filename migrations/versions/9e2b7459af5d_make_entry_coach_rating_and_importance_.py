"""make Entry coach rating and importance not nullable

Revision ID: 9e2b7459af5d
Revises: d0265c268456
Create Date: 2021-11-25 20:02:30.608739

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9e2b7459af5d'
down_revision = 'd0265c268456'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('entry', schema=None) as batch_op:
        batch_op.alter_column('coach_rating',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('coach_importance',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('entry', schema=None) as batch_op:
        batch_op.alter_column('coach_importance',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('coach_rating',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###