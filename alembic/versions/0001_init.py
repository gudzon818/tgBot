"""
Initial schema

Revision ID: 0001_init
Revises: 
Create Date: 2025-11-12
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "0001_init"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "feedbacks",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.BigInteger(), nullable=False, index=True),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_feedbacks_user_id", "feedbacks", ["user_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_feedbacks_user_id", table_name="feedbacks")
    op.drop_table("feedbacks")
