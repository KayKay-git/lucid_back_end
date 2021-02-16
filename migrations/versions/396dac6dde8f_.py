"""empty message

Revision ID: 396dac6dde8f
Revises: 78ce10a11bf0
Create Date: 2021-02-12 00:10:52.728580

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '396dac6dde8f'
down_revision = '78ce10a11bf0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_token', sa.String(), nullable=True),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=True),
    sa.Column('last_name', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('image_url', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###
