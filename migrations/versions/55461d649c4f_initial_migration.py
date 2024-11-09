"""Initial migration.

Revision ID: 55461d649c4f
Revises: 
Create Date: 2024-10-25 20:53:56.816090

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '55461d649c4f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('guarderia',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=100), nullable=True),
    sa.Column('ubicacion', sa.String(length=255), nullable=True),
    sa.Column('horarios', sa.String(length=100), nullable=True),
    sa.Column('servicios', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('usuario',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=100), nullable=True),
    sa.Column('correo', sa.String(length=100), nullable=True),
    sa.Column('telefono', sa.String(length=15), nullable=True),
    sa.Column('direccion', sa.String(length=255), nullable=True),
    sa.Column('tipo_usuario', sa.String(length=50), nullable=True),
    sa.Column('password', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('correo')
    )
    op.create_table('mascota',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=100), nullable=True),
    sa.Column('raza', sa.String(length=50), nullable=True),
    sa.Column('edad', sa.Integer(), nullable=True),
    sa.Column('peso', sa.Numeric(precision=5, scale=2), nullable=True),
    sa.Column('alergias', sa.Text(), nullable=True),
    sa.Column('vacunas', sa.Text(), nullable=True),
    sa.Column('dueño_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['dueño_id'], ['usuario.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('reserva',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('fecha', sa.Date(), nullable=True),
    sa.Column('tipo_servicio', sa.String(length=50), nullable=True),
    sa.Column('estado', sa.String(length=50), nullable=True),
    sa.Column('mascota_id', sa.Integer(), nullable=True),
    sa.Column('guarderia_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['guarderia_id'], ['guarderia.id'], ),
    sa.ForeignKeyConstraint(['mascota_id'], ['mascota.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('pago',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('monto', sa.Numeric(precision=10, scale=2), nullable=True),
    sa.Column('fecha', sa.Date(), nullable=True),
    sa.Column('metodo_pago', sa.String(length=50), nullable=True),
    sa.Column('reserva_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['reserva_id'], ['reserva.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('pago')
    op.drop_table('reserva')
    op.drop_table('mascota')
    op.drop_table('usuario')
    op.drop_table('guarderia')
    # ### end Alembic commands ###
