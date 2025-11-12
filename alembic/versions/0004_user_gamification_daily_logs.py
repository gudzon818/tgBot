"""
Add user gamification fields and daily_logs table

Revision ID: 0004_user_gamification_daily_logs
Revises: 0003_indexes
Create Date: 2025-11-12
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "0004_user_gamification_daily_logs"
down_revision = "0003_indexes"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add columns to users
    with op.batch_alter_table("users") as batch_op:
        batch_op.add_column(sa.Column("score", sa.Integer(), nullable=False, server_default="0"))
        batch_op.add_column(sa.Column("daily_streak", sa.Integer(), nullable=False, server_default="0"))
        batch_op.add_column(sa.Column("last_daily_on", sa.Date(), nullable=True))

    # Create daily_logs table
    op.create_table(
        "daily_logs",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.BigInteger(), nullable=False, index=True),
        sa.Column("day", sa.Date(), nullable=False, index=True),
        sa.Column("category", sa.String(length=32), nullable=False),
        sa.Column("difficulty", sa.String(length=16), nullable=False),
        sa.Column("status", sa.String(length=16), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
    )
    op.create_index("ix_daily_logs_user_id", "daily_logs", ["user_id"], unique=False)
    op.create_index("ix_daily_logs_day", "daily_logs", ["day"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_daily_logs_day", table_name="daily_logs")
    op.drop_index("ix_daily_logs_user_id", table_name="daily_logs")
    op.drop_table("daily_logs")
    with op.batch_alter_table("users") as batch_op:
        batch_op.drop_column("last_daily_on")
        batch_op.drop_column("daily_streak")
        batch_op.drop_column("score")
