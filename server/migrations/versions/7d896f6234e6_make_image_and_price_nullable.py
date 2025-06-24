"""Make image and price nullable

Revision ID: 7d896f6234e6
Revises: 7ffd2c2bb9ee
Create Date: 2025-06-24 06:21:13.365468

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7d896f6234e6'
down_revision = '7ffd2c2bb9ee'
branch_labels = None
depends_on = None


def upgrade():
    # Rename the original table
    op.rename_table('plants', 'plants_old')

    # Recreate the table with image and price as nullable
    op.create_table(
        'plants',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('image', sa.String, nullable=True),
        sa.Column('price', sa.Numeric(10, 2), nullable=True)
    )

    # Copy data from the old table
    op.execute(
        'INSERT INTO plants (id, name, image, price) SELECT id, name, image, price FROM plants_old'
    )

    # Drop the old table
    op.drop_table('plants_old')

def downgrade():
    op.rename_table('plants', 'plants_new')

    op.create_table(
        'plants',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('image', sa.String, nullable=False),  # back to NOT NULL
        sa.Column('price', sa.Numeric(10, 2), nullable=False)  # back to NOT NULL
    )

    op.execute(
        'INSERT INTO plants (id, name, image, price) SELECT id, name, image, price FROM plants_new'
    )

    op.drop_table('plants_new')
