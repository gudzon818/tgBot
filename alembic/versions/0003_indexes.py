"""
Add DB indexes to improve read performance

Revision ID: 0003_indexes
Revises: 0002_users
Create Date: 2025-11-12
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "0003_indexes"
down_revision = "0002_users"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # feedbacks.created_at index
    op.create_index("ix_feedbacks_created_at", "feedbacks", ["created_at"], unique=False)
    # users.username index
    op.create_index("ix_users_username", "users", ["username"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_users_username", table_name="users")
    op.drop_index("ix_feedbacks_created_at", table_name="feedbacks")
