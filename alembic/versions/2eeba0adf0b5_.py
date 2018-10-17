"""empty message

Revision ID: 2eeba0adf0b5
Revises: 03c73ce9d935
Create Date: 2018-10-17 17:58:45.243762

"""
from alembic import op
import sqlalchemy as sa
import auth.models


# revision identifiers, used by Alembic.
revision = '2eeba0adf0b5'
down_revision = '03c73ce9d935'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'password',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'password',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###
