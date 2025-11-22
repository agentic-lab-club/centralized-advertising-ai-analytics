"""add ml prediction tables

Revision ID: 002_ml_tables
Revises: 
Create Date: 2025-11-22 03:12:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '002_ml_tables'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Create ml_roi_forecast table
    op.create_table('ml_roi_forecast',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('channel', sa.String(length=50), nullable=True),
        sa.Column('roi_forecast', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ml_roi_forecast_channel'), 'ml_roi_forecast', ['channel'], unique=False)
    op.create_index(op.f('ix_ml_roi_forecast_id'), 'ml_roi_forecast', ['id'], unique=False)

    # Create ml_roi_timeseries table
    op.create_table('ml_roi_timeseries',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('date', sa.Date(), nullable=True),
        sa.Column('channel', sa.String(length=50), nullable=True),
        sa.Column('roi_actual', sa.Float(), nullable=True),
        sa.Column('conversion_actual', sa.Float(), nullable=True),
        sa.Column('roi_pred', sa.Float(), nullable=True),
        sa.Column('conversion_pred', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ml_roi_timeseries_channel'), 'ml_roi_timeseries', ['channel'], unique=False)
    op.create_index(op.f('ix_ml_roi_timeseries_id'), 'ml_roi_timeseries', ['id'], unique=False)

    # Create ml_reach_ctr_timeseries table
    op.create_table('ml_reach_ctr_timeseries',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('date', sa.Date(), nullable=True),
        sa.Column('channel', sa.String(length=50), nullable=True),
        sa.Column('reach_actual', sa.Integer(), nullable=True),
        sa.Column('ctr_actual', sa.Float(), nullable=True),
        sa.Column('reach_pred', sa.Integer(), nullable=True),
        sa.Column('ctr_pred', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ml_reach_ctr_timeseries_channel'), 'ml_reach_ctr_timeseries', ['channel'], unique=False)
    op.create_index(op.f('ix_ml_reach_ctr_timeseries_id'), 'ml_reach_ctr_timeseries', ['id'], unique=False)

    # Create ml_budget_rec table
    op.create_table('ml_budget_rec',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('channel', sa.String(length=50), nullable=True),
        sa.Column('roi_pred', sa.Float(), nullable=True),
        sa.Column('conversion_pred', sa.Float(), nullable=True),
        sa.Column('acquisition_cost', sa.Float(), nullable=True),
        sa.Column('recommended_budget', sa.Float(), nullable=True),
        sa.Column('total_budget', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ml_budget_rec_channel'), 'ml_budget_rec', ['channel'], unique=False)
    op.create_index(op.f('ix_ml_budget_rec_id'), 'ml_budget_rec', ['id'], unique=False)

def downgrade() -> None:
    op.drop_table('ml_budget_rec')
    op.drop_table('ml_reach_ctr_timeseries')
    op.drop_table('ml_roi_timeseries')
    op.drop_table('ml_roi_forecast')
