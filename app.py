import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from src.data_loader import load_pokemon_data, TYPE_COLORS, STAT_COLUMNS
from src.visualizer import (
    build_2d_radar,
    build_type_heatmap,
    build_3d_morphospace,
    build_3d_pca_manifold,
    build_4d_animated_generation_scatter,
    build_4d_battle_trajectory
)
from src.battle_engine import simulate_battle

# Page configuration
st.set_page_config(
    page_title="Pokémon 4D Stat Explorer & Arena",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom modern CSS styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Space Grotesk', -apple-system, sans-serif;
    }
    
    .metric-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7), rgba(15, 23, 42, 0.9));
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 18px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(10px);
        margin-bottom: 15px;
    }
    
    .badge-type {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 12px;
        color: white;
        text-transform: uppercase;
        margin-right: 6px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
    }
    
    .combat-log-box {
        background-color: #0b132b;
        border: 1px solid #1e293b;
        border-radius: 8px;
        padding: 12px;
        font-family: monospace;
        font-size: 13px;
        max-height: 280px;
        overflow-y: auto;
        color: #38bdf8;
    }
</style>
""", unsafe_allow_html=True)

# Load dataset
@st.cache_data
def get_data():
    return load_pokemon_data("data/pokemon.csv")

df, pca_model = get_data()

# Sidebar
st.sidebar.image("https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/25.png", width=120)
st.sidebar.title("⚡ Pokémon Telemetry")
st.sidebar.markdown("Explore 2D, 3D & 4D multi-dimensional Pokémon stats, morphospaces, and real-time battle telemetry.")

# Global Filters
st.sidebar.header("Global Filters")
gen_filter = st.sidebar.multiselect("Filter by Generation", options=sorted(df["Generation"].unique()), default=sorted(df["Generation"].unique()))
type_filter = st.sidebar.multiselect("Filter by Primary Type", options=sorted(df["Type 1"].unique()), default=[])
legendary_filter = st.sidebar.radio("Legendary Status", options=["All", "Legendary Only", "Non-Legendary Only"], index=0)

filtered_df = df[df["Generation"].isin(gen_filter)]
if type_filter:
    filtered_df = filtered_df[filtered_df["Type 1"].isin(type_filter)]
if legendary_filter == "Legendary Only":
    filtered_df = filtered_df[filtered_df["Legendary"] == True]
elif legendary_filter == "Non-Legendary Only":
    filtered_df = filtered_df[filtered_df["Legendary"] == False]

# Hero Header
col_title, col_metrics = st.columns([2, 3])
with col_title:
    st.title("Pokémon 4D Stat Explorer")
    st.caption("Multi-dimensional geometric analytics, 3D convex hull morphospaces, and dynamic 4D battle simulations.")

with col_metrics:
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    with kpi1:
        st.markdown(f"""
        <div class="metric-card">
            <span style="color: #94a3b8; font-size: 12px;">ACTIVE SPECIMENS</span>
            <h3 style="margin: 0; color: #38bdf8;">{len(filtered_df)}</h3>
        </div>
        """, unsafe_allow_html=True)
    with kpi2:
        st.markdown(f"""
        <div class="metric-card">
            <span style="color: #94a3b8; font-size: 12px;">TOP BASE STAT</span>
            <h3 style="margin: 0; color: #f59e0b;">{filtered_df['Total'].max() if len(filtered_df) > 0 else 0}</h3>
        </div>
        """, unsafe_allow_html=True)
    with kpi3:
        st.markdown(f"""
        <div class="metric-card">
            <span style="color: #94a3b8; font-size: 12px;">AVG SPEED</span>
            <h3 style="margin: 0; color: #10b981;">{round(filtered_df['Speed'].mean(), 1) if len(filtered_df) > 0 else 0}</h3>
        </div>
        """, unsafe_allow_html=True)
    with kpi4:
        st.markdown(f"""
        <div class="metric-card">
            <span style="color: #94a3b8; font-size: 12px;">LEGENDARY RATIO</span>
            <h3 style="margin: 0; color: #f43f5e;">{round((filtered_df['Legendary'].sum() / max(1, len(filtered_df))) * 100, 1)}%</h3>
        </div>
        """, unsafe_allow_html=True)

# Main Navigation Tabs
tab_2d, tab_3d, tab_4d, tab_team = st.tabs([
    "📊 2D Multi-Dimensional EDA",
    "🌐 3D Morphospace & Manifolds",
    "⏳ 4D Hyper-Dimensional Arena",
    "🛡️ Team Synergy & Polytope"
])

# ==========================================
# TAB 1: 2D MULTI-DIMENSIONAL EDA
# ==========================================
with tab_2d:
    st.subheader("Head-to-Head Comparative Radar Analysis")
    
    col_sel1, col_sel2 = st.columns(2)
    with col_sel1:
        p1_name = st.selectbox("Select Pokémon Alpha", options=df["Name"].tolist(), index=2) # Venusaur default
        p1_data = df[df["Name"] == p1_name].iloc[0]
        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 15px; margin-top: 10px;">
            <img src="{p1_data['Sprite_URL']}" width="90" style="filter: drop-shadow(0 4px 10px rgba(0,0,0,0.5));" />
            <div>
                <h4 style="margin: 0;">{p1_data['Name']} <span style="font-size: 14px; color: #94a3b8;">#{p1_data['#']}</span></h4>
                <div style="margin-top: 5px;">
                    <span class="badge-type" style="background-color: {TYPE_COLORS.get(p1_data['Type 1'], '#64748b')};">{p1_data['Type 1']}</span>
                    {f'<span class="badge-type" style="background-color: {TYPE_COLORS.get(p1_data["Type 2"], "#64748b")};">{p1_data["Type 2"]}</span>' if p1_data['Type 2'] != 'None' else ''}
                </div>
                <div style="margin-top: 5px; font-weight: bold; color: #38bdf8;">Total BST: {p1_data['Total']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with col_sel2:
        p2_name = st.selectbox("Select Pokémon Beta", options=df["Name"].tolist(), index=6) # Charizard default
        p2_data = df[df["Name"] == p2_name].iloc[0]
        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 15px; margin-top: 10px;">
            <img src="{p2_data['Sprite_URL']}" width="90" style="filter: drop-shadow(0 4px 10px rgba(0,0,0,0.5));" />
            <div>
                <h4 style="margin: 0;">{p2_data['Name']} <span style="font-size: 14px; color: #94a3b8;">#{p2_data['#']}</span></h4>
                <div style="margin-top: 5px;">
                    <span class="badge-type" style="background-color: {TYPE_COLORS.get(p2_data['Type 1'], '#64748b')};">{p2_data['Type 1']}</span>
                    {f'<span class="badge-type" style="background-color: {TYPE_COLORS.get(p2_data["Type 2"], "#64748b")};">{p2_data["Type 2"]}</span>' if p2_data['Type 2'] != 'None' else ''}
                </div>
                <div style="margin-top: 5px; font-weight: bold; color: #f43f5e;">Total BST: {p2_data['Total']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    col_radar, col_stat_diff = st.columns([3, 2])
    with col_radar:
        radar_fig = build_2d_radar(p1_data, p2_data)
        st.plotly_chart(radar_fig, use_container_width=True)
    with col_stat_diff:
        st.markdown("#### Stat Delta Analysis")
        delta_df = pd.DataFrame({
            "Stat": STAT_COLUMNS,
            p1_name: [p1_data[c] for c in STAT_COLUMNS],
            p2_name: [p2_data[c] for c in STAT_COLUMNS],
            "Advantage": [f"+{p1_data[c] - p2_data[c]} {p1_name}" if p1_data[c] > p2_data[c] else (f"+{p2_data[c] - p1_data[c]} {p2_name}" if p2_data[c] > p1_data[c] else "Tied") for c in STAT_COLUMNS]
        })
        st.dataframe(delta_df, use_container_width=True, hide_index=True)

    st.divider()
    
    col_hm, col_dist = st.columns([3, 2])
    with col_hm:
        st.plotly_chart(build_type_heatmap(), use_container_width=True)
    with col_dist:
        st.markdown("#### Stat Distributions by Generation")
        stat_choice = st.selectbox("Select Stat for Distribution", STAT_COLUMNS, index=1)
        dist_fig = px.box(
            filtered_df,
            x="Generation",
            y=stat_choice,
            color="Generation",
            points="all",
            color_discrete_sequence=px.colors.qualitative.Prism
        )
        dist_fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#f8fafc"),
            height=450,
            showlegend=False
        )
        st.plotly_chart(dist_fig, use_container_width=True)

# ==========================================
# TAB 2: 3D MORPHOSPACE & MANIFOLDS
# ==========================================
with tab_3d:
    st.subheader("3D Continuous Stat Morphospace")
    st.markdown("Visualize Pokémon specimens in continuous 3-dimensional attribute space. Points are grouped by Primary Type or Cluster Archetype.")

    col_ax1, col_ax2, col_ax3, col_opt = st.columns(4)
    with col_ax1:
        x_axis = st.selectbox("X-Axis (Spatial 1)", STAT_COLUMNS, index=1) # Attack
    with col_ax2:
        y_axis = st.selectbox("Y-Axis (Spatial 2)", STAT_COLUMNS, index=2) # Defense
    with col_ax3:
        z_axis = st.selectbox("Z-Axis (Spatial 3)", STAT_COLUMNS, index=5) # Speed
    with col_opt:
        color_choice = st.selectbox("Color Mapping", ["Type 1", "Archetype", "Generation", "Legendary"], index=0)
        show_hull = st.checkbox("Show 3D Legendary Convex Hull Envelope", value=True)

    morpho_fig = build_3d_morphospace(filtered_df, x_col=x_axis, y_col=y_axis, z_col=z_axis, color_by=color_choice, show_hull=show_hull)
    st.plotly_chart(morpho_fig, use_container_width=True)

    st.divider()
    st.subheader("Unsupervised 3D PCA Archetype Manifold")
    st.markdown("Decomposes the 6 base stats into 3 principal manifold components, categorizing all Pokémon into 5 emergent combat roles.")
    pca_fig = build_3d_pca_manifold(filtered_df)
    st.plotly_chart(pca_fig, use_container_width=True)

# ==========================================
# TAB 3: 4D HYPER-DIMENSIONAL ARENA
# ==========================================
with tab_4d:
    st.subheader("4D Hyper-Dimensional Stat Evolution (Dimensions: X × Y × Z × Color × Size × Time)")
    st.markdown("Click the **Play** button below the 3D plot to watch Pokémon stat distribution evolve across Generations 1 through 6.")
    
    anim_fig = build_4d_animated_generation_scatter(filtered_df)
    st.plotly_chart(anim_fig, use_container_width=True)

    st.divider()
    st.subheader("⚔️ Dynamic 4D Battle Trajectory Simulator")
    st.markdown("Simulate an authentic turn-based battle and observe the **real-time 3D health drain vector trajectories** through combat stat space.")

    col_b1, col_b2, col_btn = st.columns([2, 2, 1])
    with col_b1:
        b_p1 = st.selectbox("Combatant Alpha", df["Name"].tolist(), index=2, key="b1")
    with col_b2:
        b_p2 = st.selectbox("Combatant Beta", df["Name"].tolist(), index=5, key="b2")
    with col_btn:
        st.write("")
        st.write("")
        start_battle = st.button("🚀 Run Battle Simulation", type="primary", use_container_width=True)

    c1 = df[df["Name"] == b_p1].iloc[0]
    c2 = df[df["Name"] == b_p2].iloc[0]

    sim_result = simulate_battle(c1, c2)

    col_arena, col_logs = st.columns([3, 2])
    with col_arena:
        battle_fig = build_4d_battle_trajectory(sim_result["trajectory"], c1["Name"], c2["Name"])
        st.plotly_chart(battle_fig, use_container_width=True)
    with col_logs:
        st.markdown(f"#### Combat Telemetry Logs (Winner: **{sim_result['winner']}** in {sim_result['turns']} Turns)")
        log_html = "<div class='combat-log-box'>" + "<br>".join(sim_result["combat_log"]) + "</div>"
        st.markdown(log_html, unsafe_allow_html=True)
        
        st.markdown("#### Final Specimen Status")
        st.write(f"**{c1['Name']}** Remaining HP: `{sim_result['p1_final']['hp']} / {c1['HP']}`")
        st.progress(max(0.0, sim_result['p1_final']['hp'] / c1['HP']))
        st.write(f"**{c2['Name']}** Remaining HP: `{sim_result['p2_final']['hp']} / {c2['HP']}`")
        st.progress(max(0.0, sim_result['p2_final']['hp'] / c2['HP']))

# ==========================================
# TAB 4: TEAM SYNERGY & POLYTOPE ANALYZER
# ==========================================
with tab_team:
    st.subheader("Competitive 6-Member Team Polytope & Vulnerability Matrix")
    st.markdown("Assemble a battle team of up to 6 Pokémon to compute multi-stat team geometry and elemental defensive coverage.")

    team_selection = st.multiselect(
        "Select Your Battle Roster (Max 6)",
        options=df["Name"].tolist(),
        default=["Gengar", "Dragonite", "Gyarados", "Lucario", "Tyranitar", "Alakazam"],
        max_selections=6
    )

    if team_selection:
        team_df = df[df["Name"].isin(team_selection)]
        
        # Display team cards
        cols = st.columns(len(team_df))
        for idx, (_, poke) in enumerate(team_df.iterrows()):
            with cols[idx]:
                st.markdown(f"""
                <div class="metric-card" style="text-align: center; padding: 10px;">
                    <img src="{poke['Sprite_URL']}" width="70" />
                    <div style="font-weight: 700; font-size: 14px; margin-top: 5px;">{poke['Name']}</div>
                    <div style="margin-top: 4px;">
                        <span class="badge-type" style="background-color: {TYPE_COLORS.get(poke['Type 1'], '#64748b')}; font-size: 10px;">{poke['Type 1']}</span>
                    </div>
                    <div style="font-size: 12px; color: #38bdf8; margin-top: 4px;">BST {poke['Total']}</div>
                </div>
                """, unsafe_allow_html=True)
                
        # Team average stats radar
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            st.markdown("#### Team Geometric Polytope (Average Core Stats)")
            team_avg = team_df[STAT_COLUMNS].mean()
            team_fig = go.Figure()
            r_team = team_avg.tolist() + [team_avg.tolist()[0]]
            cats_team = STAT_COLUMNS + [STAT_COLUMNS[0]]
            team_fig.add_trace(go.Scatterpolar(
                r=r_team,
                theta=cats_team,
                fill='toself',
                fillcolor="rgba(56, 189, 248, 0.35)",
                line=dict(color="#38bdf8", width=3),
                name="Team Average"
            ))
            team_fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 160], gridcolor="rgba(255,255,255,0.15)")),
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#f8fafc"),
                height=380,
                margin=dict(l=30, r=30, t=30, b=30)
            )
            st.plotly_chart(team_fig, use_container_width=True)
            
        with col_t2:
            st.markdown("#### Team Archetype Composition")
            arch_counts = team_df["Archetype"].value_counts().reset_index()
            arch_counts.columns = ["Archetype", "Count"]
            arch_fig = px.pie(
                arch_counts,
                names="Archetype",
                values="Count",
                hole=0.45,
                color_discrete_sequence=["#38bdf8", "#f43f5e", "#10b981", "#a855f7", "#f59e0b"]
            )
            arch_fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#f8fafc"),
                height=380,
                margin=dict(l=20, r=20, t=20, b=20)
            )
            st.plotly_chart(arch_fig, use_container_width=True)
    else:
        st.info("Select at least 1 Pokémon to evaluate team synergy.")
