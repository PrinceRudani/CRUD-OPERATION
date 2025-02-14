"""empty message

Revision ID: 2c9d25b0315a
Revises: 
Create Date: 2025-02-11 10:55:11.348954

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2c9d25b0315a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sub_category_table',
    sa.Column('sub_category_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.Column('sub_category_name', sa.String(length=100), nullable=False),
    sa.Column('sub_category_description', sa.String(length=1000), nullable=False),
    sa.Column('is_delete', sa.Boolean(), nullable=False),
    sa.Column('create_at', sa.Integer(), nullable=True),
    sa.Column('modify_at', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['category_table.category_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('sub_category_id')
    )
    op.create_table('product_table',
    sa.Column('product_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('product_category_id', sa.Integer(), nullable=False),
    sa.Column('product_sub_category_id', sa.Integer(), nullable=False),
    sa.Column('product_name', sa.String(length=100), nullable=False),
    sa.Column('product_price', sa.Float(), nullable=False),
    sa.Column('product_description', sa.String(length=1000), nullable=False),
    sa.Column('product_image_name', sa.String(length=255), nullable=False),
    sa.Column('product_image_path', sa.String(length=500), nullable=False),
    sa.Column('product_quantity', sa.Integer(), nullable=False),
    sa.Column('is_delete', sa.Boolean(), nullable=False),
    sa.Column('create_at', sa.Integer(), nullable=False),
    sa.Column('modify_at', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['product_category_id'], ['category_table.category_id'], ),
    sa.ForeignKeyConstraint(['product_sub_category_id'], ['sub_category_table.sub_category_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('product_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('product_table')
    op.drop_table('sub_category_table')
    # ### end Alembic commands ###
