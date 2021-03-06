"""association.

Revision ID: 78ce10a11bf0
Revises: f34a24ae0f77
Create Date: 2021-02-09 01:03:10.762881

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '78ce10a11bf0'
down_revision = 'f34a24ae0f77'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product', sa.Column('ingredient_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'product', 'ingredient', ['ingredient_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'product', type_='foreignkey')
    op.drop_column('product', 'ingredient_id')
    # ### end Alembic commands ###
