"""update user table

Revision ID: cdb2deb04b2a
Revises: 
Create Date: 2018-10-17 11:58:51.836908

"""
from alembic import op
import sqlalchemy as sa
import auth.models


# revision identifiers, used by Alembic.
revision = 'cdb2deb04b2a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('first_name', sa.Unicode(length=30), nullable=True))
    op.add_column('users', sa.Column('last_name', sa.Unicode(length=30), nullable=True))
    op.alter_column('users', 'email',
               existing_type=sa.VARCHAR(length=128),
               nullable=False)
    op.alter_column('users', 'password',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('users', 'username',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'username',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('users', 'password',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('users', 'email',
               existing_type=sa.VARCHAR(length=128),
               nullable=True)
    op.drop_column('users', 'last_name')
    op.drop_column('users', 'first_name')
    # ### end Alembic commands ###