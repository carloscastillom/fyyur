"""empty message

Revision ID: 60fa1ba131a0
Revises: cec62a2f0173
Create Date: 2021-01-31 14:59:46.263841

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '60fa1ba131a0'
down_revision = 'cec62a2f0173'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('genre',
    sa.Column('id', sa.String(length=120), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('artist_genre',
    sa.Column('artist_id', sa.Integer(), nullable=False),
    sa.Column('genre_id', sa.VARCHAR(length=120), nullable=False),
    sa.ForeignKeyConstraint(['artist_id'], ['artist.id'], ),
    sa.ForeignKeyConstraint(['genre_id'], ['genre.id'], ),
    sa.PrimaryKeyConstraint('artist_id', 'genre_id')
    )
    op.create_table('venue_genre',
    sa.Column('venue_id', sa.Integer(), nullable=False),
    sa.Column('genre_id', sa.VARCHAR(length=120), nullable=False),
    sa.ForeignKeyConstraint(['genre_id'], ['genre.id'], ),
    sa.ForeignKeyConstraint(['venue_id'], ['venue.id'], ),
    sa.PrimaryKeyConstraint('venue_id', 'genre_id')
    )
    op.drop_column('artist', 'genres')
    op.drop_column('venue', 'genres')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('venue', sa.Column('genres', sa.VARCHAR(length=120), autoincrement=False, nullable=True))
    op.add_column('artist', sa.Column('genres', sa.VARCHAR(length=120), autoincrement=False, nullable=True))
    op.drop_table('venue_genre')
    op.drop_table('artist_genre')
    op.drop_table('genre')
    # ### end Alembic commands ###
