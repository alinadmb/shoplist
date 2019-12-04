"""add table lists and table items

Revision ID: 62416bc0c673
Revises: 39aa5d2cfe79
Create Date: 2019-12-02 01:26:22.380371

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '62416bc0c673'
down_revision = '39aa5d2cfe79'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('item',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('itemname', sa.String(length=30), nullable=True),
    sa.Column('list_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['list_id'], ['list.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_item_itemname'), 'item', ['itemname'], unique=False)
    op.add_column('list', sa.Column('listname', sa.String(length=30), nullable=True))
    op.create_index(op.f('ix_list_listname'), 'list', ['listname'], unique=False)
    op.drop_index('ix_list_item', table_name='list')
    op.drop_index('ix_list_name', table_name='list')
    op.drop_column('list', 'name')
    op.drop_column('list', 'item')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('list', sa.Column('item', sa.VARCHAR(length=30), nullable=True))
    op.add_column('list', sa.Column('name', sa.VARCHAR(length=30), nullable=True))
    op.create_index('ix_list_name', 'list', ['name'], unique=False)
    op.create_index('ix_list_item', 'list', ['item'], unique=False)
    op.drop_index(op.f('ix_list_listname'), table_name='list')
    op.drop_column('list', 'listname')
    op.drop_index(op.f('ix_item_itemname'), table_name='item')
    op.drop_table('item')
    # ### end Alembic commands ###
