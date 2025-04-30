from sqlalchemy.sql import table, column
from sqlalchemy import Integer, String

def upgrade():
    # Cria tabela de categorias
    op.create_table(
        'categoria',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('nome', sa.String(50), nullable=False),
    )

    # Insere uma categoria padrão
    categoria_table = table('categoria',
        column('id', Integer),
        column('nome', String)
    )
    op.bulk_insert(categoria_table, [{'id': 1, 'nome': 'Sem Categoria'}])

    # Adiciona campo categoria_id como nullable inicialmente
    with op.batch_alter_table('produto') as batch_op:
        batch_op.add_column(sa.Column('categoria_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_categoria', 'categoria', ['categoria_id'], ['id'])

    # Atualiza produtos existentes para usar a categoria padrão
    op.execute('UPDATE produto SET categoria_id = 1')

    # Torna o campo NOT NULL
    with op.batch_alter_table('produto') as batch_op:
        batch_op.alter_column('categoria_id', nullable=False)
