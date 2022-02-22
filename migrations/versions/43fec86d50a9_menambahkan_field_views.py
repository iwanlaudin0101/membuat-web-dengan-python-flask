"""menambahkan field views

Revision ID: 43fec86d50a9
Revises: 3b141c68f3a4
Create Date: 2022-02-21 15:36:20.655293

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '43fec86d50a9'
down_revision = '3b141c68f3a4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('blog', sa.Column('views', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('blog', 'views')
    # ### end Alembic commands ###
