"""Adiciona tabela de categorias

Revision ID: 1c018f4af86d
Revises: b1a581a764d6
Create Date: 2025-04-29 17:23:47.277350

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1c018f4af86d'
down_revision = 'b1a581a764d6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('produto', schema=None) as batch_op:
        batch_op.add_column(sa.Column('categoria_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key('fk_produto_categoria', 'categoria', ['categoria_id'], ['id'])
        batch_op.drop_column('categoria')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('produto', schema=None) as batch_op:
        batch_op.add_column(sa.Column('categoria', sa.VARCHAR(length=100), nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('categoria_id')

    # ### end Alembic commands ###
