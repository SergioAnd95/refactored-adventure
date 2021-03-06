"""empty message

Revision ID: 7a9fec7f7f2d
Revises: 2eeba0adf0b5
Create Date: 2018-10-17 18:06:59.603359

"""
from alembic import op
import sqlalchemy as sa
import auth.models


# revision identifiers, used by Alembic.
revision = '7a9fec7f7f2d'
down_revision = '2eeba0adf0b5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'users', ['email'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    # ### end Alembic commands ###
