"""Add column side to Stock model

Revision ID: 7b3b9305c642
Revises: c12aae1735e9
Create Date: 2022-05-28 08:40:22.953027

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7b3b9305c642'
down_revision = 'c12aae1735e9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('stock', sa.Column('side', sa.Enum('buy', 'sell', name='side'), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('stock', 'side')
    # ### end Alembic commands ###
