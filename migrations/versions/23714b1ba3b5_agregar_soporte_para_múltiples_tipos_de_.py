"""Agregar soporte para múltiples tipos de servicio

Revision ID: 23714b1ba3b5
Revises: 55461d649c4f
Create Date: 2024-10-26 15:24:45.242982

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '23714b1ba3b5'
down_revision = '55461d649c4f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('reserva_servicio')
    op.drop_table('servicios')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('servicios',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('servicios_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('nombre', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='servicios_pkey'),
    sa.UniqueConstraint('nombre', name='servicios_nombre_key'),
    postgresql_ignore_search_path=False
    )
    op.create_table('reserva_servicio',
    sa.Column('reserva_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('servicio_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['reserva_id'], ['reserva.id'], name='reserva_servicio_reserva_id_fkey'),
    sa.ForeignKeyConstraint(['servicio_id'], ['servicios.id'], name='reserva_servicio_servicio_id_fkey'),
    sa.PrimaryKeyConstraint('reserva_id', 'servicio_id', name='reserva_servicio_pkey')
    )
    # ### end Alembic commands ###
