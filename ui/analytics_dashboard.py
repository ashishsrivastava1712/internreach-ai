import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def render_analytics_tab(db_manager):
    st.header("📊 Campaign Analytics")

    try:
        # Get all emails from DB
        emails = db_manager.get_all_emails() if hasattr(db_manager, 'get_all_emails') else []

        if not emails:
            st.info("No campaign data yet. Run a campaign first!")
            return

        df = pd.DataFrame(emails)

        # ── Summary Cards ──
        col1, col2, col3, col4 = st.columns(4)
        total   = len(df)
        sent    = len(df[df['status'] == 'sent'])    if 'status' in df.columns else 0
        replied = len(df[df['status'] == 'replied']) if 'status' in df.columns else 0
        pending = total - sent

        col1.metric("Total Emails",   total)
        col2.metric("Sent",           sent)
        col3.metric("Replies",        replied)
        col4.metric("Pending",        pending)

        st.divider()

        # ── Status Chart ──
        if 'status' in df.columns:
            status_counts = df['status'].value_counts().reset_index()
            status_counts.columns = ['Status', 'Count']
            fig = px.pie(status_counts, values='Count', names='Status',
                         title='Email Status Distribution',
                         color_discrete_sequence=px.colors.sequential.Blues_r)
            st.plotly_chart(fig, use_container_width=True)

        # ── Company Table ──
        st.subheader("📋 Email Details")
        cols = [c for c in ['company', 'hr_name', 'subject', 'status', 'sent_at'] if c in df.columns]
        if cols:
            st.dataframe(df[cols], use_container_width=True)

    except Exception as e:
        st.error(f"Analytics error: {e}")