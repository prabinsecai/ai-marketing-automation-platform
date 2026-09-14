"""initial_schema

Revision ID: 001_initial_schema
Revises:
Create Date: 2026-09-14 21:30:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '001_initial_schema'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Workspaces
    op.create_table(
        'workspaces',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('slug', sa.String(length=255), nullable=False),
        sa.Column('industry', sa.String(length=100), nullable=True),
        sa.Column('website', sa.String(length=255), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('brand_guidelines', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_workspaces_slug'), 'workspaces', ['slug'], unique=True)

    # 2. Users
    op.create_table(
        'users',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('workspace_id', sa.String(length=36), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('full_name', sa.String(length=255), nullable=False),
        sa.Column('role', sa.String(length=50), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['workspace_id'], ['workspaces.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_workspace_id'), 'users', ['workspace_id'], unique=False)

    # 3. Products
    op.create_table(
        'products',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('workspace_id', sa.String(length=36), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('category', sa.String(length=100), nullable=True),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('price', sa.String(length=100), nullable=True),
        sa.Column('features', sa.JSON(), nullable=False),
        sa.Column('target_benefits', sa.JSON(), nullable=False),
        sa.Column('usp', sa.Text(), nullable=True),
        sa.Column('url', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['workspace_id'], ['workspaces.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_products_workspace_id'), 'products', ['workspace_id'], unique=False)

    # 4. Audiences
    op.create_table(
        'audiences',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('workspace_id', sa.String(length=36), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('demographics', sa.JSON(), nullable=False),
        sa.Column('pain_points', sa.JSON(), nullable=False),
        sa.Column('interests', sa.JSON(), nullable=False),
        sa.Column('goals', sa.JSON(), nullable=False),
        sa.Column('preferred_channels', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['workspace_id'], ['workspaces.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_audiences_workspace_id'), 'audiences', ['workspace_id'], unique=False)

    # 5. Campaigns
    op.create_table(
        'campaigns',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('workspace_id', sa.String(length=36), nullable=False),
        sa.Column('product_id', sa.String(length=36), nullable=True),
        sa.Column('audience_id', sa.String(length=36), nullable=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('objective', sa.String(length=255), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('budget', sa.String(length=100), nullable=True),
        sa.Column('target_timeline', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['audience_id'], ['audiences.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['product_id'], ['products.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['workspace_id'], ['workspaces.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_campaigns_status'), 'campaigns', ['status'], unique=False)
    op.create_index(op.f('ix_campaigns_workspace_id'), 'campaigns', ['workspace_id'], unique=False)

    # 6. Campaign Strategies
    op.create_table(
        'campaign_strategies',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('campaign_id', sa.String(length=36), nullable=False),
        sa.Column('summary', sa.Text(), nullable=False),
        sa.Column('audience_reasoning', sa.Text(), nullable=False),
        sa.Column('positioning', sa.Text(), nullable=False),
        sa.Column('key_message', sa.Text(), nullable=False),
        sa.Column('channel_strategy', sa.JSON(), nullable=False),
        sa.Column('campaign_themes', sa.JSON(), nullable=False),
        sa.Column('content_recommendations', sa.JSON(), nullable=False),
        sa.Column('cta_strategy', sa.Text(), nullable=False),
        sa.Column('timeline_suggestion', sa.Text(), nullable=False),
        sa.Column('future_success_metrics', sa.JSON(), nullable=False),
        sa.Column('risks_assumptions', sa.JSON(), nullable=False),
        sa.Column('raw_prompt', sa.Text(), nullable=True),
        sa.Column('raw_response', sa.Text(), nullable=True),
        sa.Column('model_used', sa.String(length=100), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['campaign_id'], ['campaigns.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_campaign_strategies_campaign_id'), 'campaign_strategies', ['campaign_id'], unique=True)

    # 7. Content Assets
    op.create_table(
        'content_assets',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('campaign_id', sa.String(length=36), nullable=False),
        sa.Column('channel', sa.String(length=50), nullable=False),
        sa.Column('variation_number', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=True),
        sa.Column('preview_text', sa.Text(), nullable=True),
        sa.Column('body', sa.Text(), nullable=False),
        sa.Column('hook', sa.Text(), nullable=True),
        sa.Column('cta', sa.String(length=255), nullable=True),
        sa.Column('hashtags', sa.JSON(), nullable=False),
        sa.Column('platform', sa.String(length=50), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('is_selected', sa.Boolean(), nullable=False),
        sa.Column('edit_history', sa.JSON(), nullable=False),
        sa.Column('raw_prompt', sa.Text(), nullable=True),
        sa.Column('raw_response', sa.Text(), nullable=True),
        sa.Column('model_used', sa.String(length=100), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['campaign_id'], ['campaigns.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_content_assets_campaign_id'), 'content_assets', ['campaign_id'], unique=False)
    op.create_index(op.f('ix_content_assets_channel'), 'content_assets', ['channel'], unique=False)
    op.create_index(op.f('ix_content_assets_status'), 'content_assets', ['status'], unique=False)

    # 8. Approvals
    op.create_table(
        'approvals',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('workspace_id', sa.String(length=36), nullable=False),
        sa.Column('campaign_id', sa.String(length=36), nullable=False),
        sa.Column('content_asset_id', sa.String(length=36), nullable=True),
        sa.Column('user_id', sa.String(length=36), nullable=True),
        sa.Column('action', sa.String(length=50), nullable=False),
        sa.Column('feedback', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['campaign_id'], ['campaigns.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['content_asset_id'], ['content_assets.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['workspace_id'], ['workspaces.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_approvals_campaign_id'), 'approvals', ['campaign_id'], unique=False)
    op.create_index(op.f('ix_approvals_content_asset_id'), 'approvals', ['content_asset_id'], unique=False)
    op.create_index(op.f('ix_approvals_workspace_id'), 'approvals', ['workspace_id'], unique=False)

    # 9. AI Logs
    op.create_table(
        'ai_logs',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('workspace_id', sa.String(length=36), nullable=False),
        sa.Column('campaign_id', sa.String(length=36), nullable=True),
        sa.Column('agent_name', sa.String(length=100), nullable=False),
        sa.Column('provider', sa.String(length=50), nullable=False),
        sa.Column('model', sa.String(length=100), nullable=False),
        sa.Column('prompt_template', sa.String(length=100), nullable=True),
        sa.Column('prompt_preview', sa.Text(), nullable=True),
        sa.Column('response_preview', sa.Text(), nullable=True),
        sa.Column('prompt_tokens', sa.Integer(), nullable=False),
        sa.Column('completion_tokens', sa.Integer(), nullable=False),
        sa.Column('total_tokens', sa.Integer(), nullable=False),
        sa.Column('latency_ms', sa.Integer(), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['campaign_id'], ['campaigns.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['workspace_id'], ['workspaces.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ai_logs_created_at'), 'ai_logs', ['created_at'], unique=False)
    op.create_index(op.f('ix_ai_logs_workspace_id'), 'ai_logs', ['workspace_id'], unique=False)


def downgrade() -> None:
    op.drop_table('ai_logs')
    op.drop_table('approvals')
    op.drop_table('content_assets')
    op.drop_table('campaign_strategies')
    op.drop_table('campaigns')
    op.drop_table('audiences')
    op.drop_table('products')
    op.drop_table('users')
    op.drop_table('workspaces')
