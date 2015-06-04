"""Initial migration

Revision ID: 470bbf654408
Revises: None
Create Date: 2015-06-04 17:58:52.142024

"""

# revision identifiers, used by Alembic.
revision = '470bbf654408'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('shows',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('episode', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=160), nullable=True),
    sa.Column('dt', sa.DateTime(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('url', sa.String(length=320), nullable=True),
    sa.Column('file', sa.String(length=320), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('shows')
    ### end Alembic commands ###
