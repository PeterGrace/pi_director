"""create users table for auth

Revision ID: 41c29db70997
Revises: 25a9a37f3c5f
Create Date: 2015-08-31 21:18:32.202369

"""

# revision identifiers, used by Alembic.
revision = '41c29db70997'
down_revision = '25a9a37f3c5f'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.Text(), nullable=True),
    sa.Column('AccessLevel', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_index('EmailIndex', 'Users', ['email'], unique=True, mysql_length=255)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('EmailIndex', table_name='Users')
    op.drop_table('Users')
    ### end Alembic commands ###
