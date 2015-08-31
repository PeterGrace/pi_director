"""add last seen column to data model

Revision ID: 2345bcfeaced
Revises: 1544be55e36c
Create Date: 2015-08-31 14:27:33.503089

"""

# revision identifiers, used by Alembic.
revision = '2345bcfeaced'
down_revision = '1544be55e36c'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('PiUrl', sa.Column('lastseen', sa.DateTime(), nullable=True))


def downgrade():
    op.drop_column('PiUrl', 'lastseen')

