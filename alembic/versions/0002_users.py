"""
Add users table for persistent i18n

Revision ID: 0002_users
Revises: 0001_init
Create Date: 2025-11-12
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "0002_users"
down_revision = "0001_init"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("user_id", sa.BigInteger(), primary_key=True, nullable=False),
        sa.Column("username", sa.String(length=64), nullable=True),
        sa.Column("language_code", sa.String(length=8), nullable=False, server_default="ru"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("users")
