"""empty message

Revision ID: 036c36cae680
Revises: 90e784fe9d52
Create Date: 2021-02-24 15:52:24.770416

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '036c36cae680'
down_revision = '90e784fe9d52'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('book',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('book_name', sa.String(length=50), nullable=False),
    sa.Column('publisher', sa.String(length=50), nullable=False),
    sa.Column('author', sa.String(length=50), nullable=False),
    sa.Column('publication_date', sa.DateTime(), nullable=False),
    sa.Column('pages', sa.Integer(), nullable=False),
    sa.Column('isbn', sa.Integer(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('link', sa.String(length=50), nullable=False),
    sa.Column('img_url', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id', 'isbn'),
    sa.UniqueConstraint('book_name'),
    sa.UniqueConstraint('isbn')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('book')
    # ### end Alembic commands ###
