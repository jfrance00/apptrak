"""empty message

Revision ID: 410128b2bb69
Revises: 0a515372c0ac
Create Date: 2020-08-23 19:23:36.151066

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '410128b2bb69'
down_revision = '0a515372c0ac'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('job_application', sa.Column('date_added', sa.Date(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('job_application', 'date_added')
    # ### end Alembic commands ###