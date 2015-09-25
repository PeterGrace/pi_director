"""Add Logs table per Dan's commit

Revision ID: 3685d41416bc
Revises: 43e4ec819875
Create Date: 2015-09-25 01:46:43.351516

"""

# revision identifiers, used by Alembic.
revision = '3685d41416bc'
down_revision = '43e4ec819875'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('Logs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('filename', sa.Text(), nullable=True),
    sa.Column('log', sa.Text(), nullable=True),
    sa.Column('uuid', sa.Text(), nullable=True),
    op.create_foreign_key(None, 'Logs', 'PiUrl', ['uuid'], ['uuid']),    
    sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('Logs')
    pass
