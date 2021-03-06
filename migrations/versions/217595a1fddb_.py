"""empty message

Revision ID: 217595a1fddb
Revises: 
Create Date: 2017-09-21 12:00:39.826600

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '217595a1fddb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('memories',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('do_time', sa.DateTime(), nullable=True),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('is_done', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('memories')
    # ### end Alembic commands ###
