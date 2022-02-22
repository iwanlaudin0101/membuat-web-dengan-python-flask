"""menambahkan ondelete cascade

Revision ID: 05e9d3361e1b
Revises: 9d15c8885224
Create Date: 2022-02-14 19:47:15.661220

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '05e9d3361e1b'
down_revision = '9d15c8885224'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('mahasiswa_ibfk_2', 'mahasiswa', type_='foreignkey')
    op.drop_constraint('mahasiswa_ibfk_1', 'mahasiswa', type_='foreignkey')
    op.create_foreign_key(None, 'mahasiswa', 'dosen', ['dosen_dua'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'mahasiswa', 'dosen', ['dosen_satu'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'mahasiswa', type_='foreignkey')
    op.drop_constraint(None, 'mahasiswa', type_='foreignkey')
    op.create_foreign_key('mahasiswa_ibfk_1', 'mahasiswa', 'dosen', ['dosen_dua'], ['id'])
    op.create_foreign_key('mahasiswa_ibfk_2', 'mahasiswa', 'dosen', ['dosen_satu'], ['id'])
    # ### end Alembic commands ###
