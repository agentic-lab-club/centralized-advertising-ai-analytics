"""Add ML predictions tables

Revision ID: 002_ml_predictions
Revises: 001_initial_tables
Create Date: 2025-11-22 03:03:20.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = '002_ml_predictions'
down_revision = '001_initial_tables'
branch_labels = None
depends_on = None

def upgrade():
    # ML ROI Forecast table
    op.create_table('ml_roi_forecast',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('channel', sa.String(length=50), nullable=True),
        sa.Column('roi_forecast', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ml_roi_forecast_channel'), 'ml_roi_forecast', ['channel'], unique=False)

    # ML ROI TimeSeries table
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

    # ML Reach CTR TimeSeries table
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

    # ML Budget Recommendation table
    op.create_table('ml_budget_recommendation',
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
    op.create_index(op.f('ix_ml_budget_recommendation_channel'), 'ml_budget_recommendation', ['channel'], unique=False)

def downgrade():
    op.drop_index(op.f('ix_ml_budget_recommendation_channel'), table_name='ml_budget_recommendation')
    op.drop_table('ml_budget_recommendation')
    op.drop_index(op.f('ix_ml_reach_ctr_timeseries_channel'), table_name='ml_reach_ctr_timeseries')
    op.drop_table('ml_reach_ctr_timeseries')
    op.drop_index(op.f('ix_ml_roi_timeseries_channel'), table_name='ml_roi_timeseries')
    op.drop_table('ml_roi_timeseries')
    op.drop_index(op.f('ix_ml_roi_forecast_channel'), table_name='ml_roi_forecast')
    op.drop_table('ml_roi_forecast')
