import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
from scipy.spatial import ConvexHull
from .data_loader import TYPE_COLORS, STAT_COLUMNS, TYPE_EFFECTIVENESS

def build_2d_radar(p1_row, p2_row=None):
    """Builds a comparison 2D radar chart for one or two Pokémon."""
    categories = STAT_COLUMNS
    fig = go.Figure()

    r1 = [p1_row[c] for c in categories]
    r1.append(r1[0]) # close polygon
    cats1 = categories + [categories[0]]
    
    color1 = TYPE_COLORS.get(p1_row["Type 1"], "#4ade80")
    fig.add_trace(go.Scatterpolar(
        r=r1,
        theta=cats1,
        fill='toself',
        fillcolor=f"rgba({int(color1[1:3],16)}, {int(color1[3:5],16)}, {int(color1[5:7],16)}, 0.4)",
        line=dict(color=color1, width=3),
        name=f"{p1_row['Name']} ({p1_row['Type 1']})"
    ))

    if p2_row is not None:
        r2 = [p2_row[c] for c in categories]
        r2.append(r2[0])
        color2 = TYPE_COLORS.get(p2_row["Type 1"], "#f43f5e")
        fig.add_trace(go.Scatterpolar(
            r=r2,
            theta=cats1,
            fill='toself',
            fillcolor=f"rgba({int(color2[1:3],16)}, {int(color2[3:5],16)}, {int(color2[5:7],16)}, 0.4)",
            line=dict(color=color2, width=3),
            name=f"{p2_row['Name']} ({p2_row['Type 1']})"
        ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 260], gridcolor="rgba(255,255,255,0.15)"),
            angularaxis=dict(gridcolor="rgba(255,255,255,0.15)", linecolor="rgba(255,255,255,0.3)")
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#f8fafc", family="Inter, sans-serif"),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
        margin=dict(l=40, r=40, t=30, b=40),
        height=380
    )
    return fig

def build_type_heatmap():
    """Builds an 18x18 interactive combat effectiveness heatmap."""
    types = list(TYPE_EFFECTIVENESS.keys())
    matrix = np.ones((len(types), len(types)))

    for i, atk in enumerate(types):
        for j, dfn in enumerate(types):
            matrix[i][j] = TYPE_EFFECTIVENESS.get(atk, {}).get(dfn, 1.0)

    fig = go.Figure(data=go.Heatmap(
        z=matrix,
        x=types,
        y=types,
        colorscale=[
            [0.0, "#0f172a"],    # 0x Immune
            [0.25, "#38bdf8"],   # 0.5x Not effective
            [0.5, "#334155"],    # 1.0x Normal
            [1.0, "#f43f5e"]     # 2.0x Super effective
        ],
        colorbar=dict(title="Multiplier", tickvals=[0, 0.5, 1.0, 2.0], ticktext=["0x (Immune)", "0.5x", "1.0x", "2.0x (Weak)"]),
        hoverongaps=False
    ))

    fig.update_layout(
        title="18x18 Pokémon Type Combat Effectiveness Matrix",
        xaxis_title="Defending Type",
        yaxis_title="Attacking Type",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#f8fafc", family="Inter, sans-serif"),
        height=550,
        margin=dict(l=60, r=40, t=50, b=60)
    )
    return fig

def build_3d_morphospace(df, x_col="Attack", y_col="Defense", z_col="Speed", color_by="Type 1", show_hull=True):
    """
    Builds a 3D Morphospace scatter plot with glowing points and optional 3D convex hull surface mesh.
    """
    fig = go.Figure()

    # Add points grouped by color_by (Type 1 or Archetype)
    for group_name, group_df in df.groupby(color_by):
        c_hex = TYPE_COLORS.get(group_name, "#38bdf8")
        custom_data = np.stack((group_df["Name"], group_df["Type 1"], group_df["Type 2"], group_df["Total"], group_df["HP"]), axis=-1)
        
        fig.add_trace(go.Scatter3d(
            x=group_df[x_col],
            y=group_df[y_col],
            z=group_df[z_col],
            mode='markers',
            name=str(group_name),
            marker=dict(
                size=6,
                color=c_hex if color_by == "Type 1" else None,
                opacity=0.85,
                line=dict(color="rgba(255,255,255,0.6)", width=1)
            ),
            customdata=custom_data,
            hovertemplate="<b>%{customdata[0]}</b><br>Type: %{customdata[1]} / %{customdata[2]}<br>Total: %{customdata[3]}<br>" +
                          f"{x_col}: " + "%{x}<br>" +
                          f"{y_col}: " + "%{y}<br>" +
                          f"{z_col}: " + "%{z}<extra></extra>"
        ))

    # Add 3D Convex Hull mesh for Legendary Pokémon
    if show_hull:
        leg_df = df[df["Legendary"] == True]
        pts = leg_df[[x_col, y_col, z_col]].dropna().values
        if len(pts) >= 4:
            try:
                hull = ConvexHull(pts)
                fig.add_trace(go.Mesh3d(
                    x=pts[:, 0],
                    y=pts[:, 1],
                    z=pts[:, 2],
                    i=hull.simplices[:, 0],
                    j=hull.simplices[:, 1],
                    k=hull.simplices[:, 2],
                    color="#f59e0b",
                    opacity=0.18,
                    name="Legendary Envelope (Convex Hull)",
                    showlegend=True
                ))
            except Exception:
                pass

    fig.update_layout(
        scene=dict(
            xaxis=dict(title=x_col, backgroundcolor="#0f172a", gridcolor="rgba(255,255,255,0.1)", showbackground=True),
            yaxis=dict(title=y_col, backgroundcolor="#0f172a", gridcolor="rgba(255,255,255,0.1)", showbackground=True),
            zaxis=dict(title=z_col, backgroundcolor="#0f172a", gridcolor="rgba(255,255,255,0.1)", showbackground=True),
            camera=dict(eye=dict(x=1.6, y=1.6, z=1.3))
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#f8fafc", family="Inter, sans-serif"),
        height=620,
        margin=dict(l=10, r=10, t=10, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5)
    )
    return fig

def build_3d_pca_manifold(df):
    """Builds a 3D PCA Stat Manifold showing the natural archetype clusters."""
    fig = px.scatter_3d(
        df,
        x="PCA_1",
        y="PCA_2",
        z="PCA_3",
        color="Archetype",
        hover_name="Name",
        hover_data={"Type 1": True, "Total": True, "HP": True, "Attack": True, "Defense": True, "Speed": True, "PCA_1": False, "PCA_2": False, "PCA_3": False},
        color_discrete_sequence=["#38bdf8", "#f43f5e", "#10b981", "#a855f7", "#f59e0b"],
        opacity=0.85
    )
    fig.update_traces(marker=dict(size=5, line=dict(color="rgba(255,255,255,0.5)", width=0.8)))
    fig.update_layout(
        title="3D PCA Archetype Manifold (Unsupervised Stat Clustering)",
        scene=dict(
            xaxis=dict(title="PCA 1 (Raw Power / Stat Mass)", backgroundcolor="#0f172a", gridcolor="rgba(255,255,255,0.1)", showbackground=True),
            yaxis=dict(title="PCA 2 (Defense vs Offense Bias)", backgroundcolor="#0f172a", gridcolor="rgba(255,255,255,0.1)", showbackground=True),
            zaxis=dict(title="PCA 3 (Special vs Physical Polar)", backgroundcolor="#0f172a", gridcolor="rgba(255,255,255,0.1)", showbackground=True)
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#f8fafc", family="Inter, sans-serif"),
        height=600,
        margin=dict(l=10, r=10, t=40, b=10)
    )
    return fig

def build_4d_animated_generation_scatter(df):
    """
    Builds a 4D Animated Hyper-Scatter:
    - Dim 1 (X): Attack
    - Dim 2 (Y): Defense
    - Dim 3 (Z): Speed
    - Dim 4 (Color): Total Base Stats
    - Dim 5 (Size): HP
    - Dim 6 (Time / Frame Animation): Generation (Gen 1 -> Gen 6)
    """
    df_anim = df.sort_values(by="Generation").copy()
    fig = px.scatter_3d(
        df_anim,
        x="Attack",
        y="Defense",
        z="Speed",
        color="Total",
        size="HP",
        size_max=22,
        animation_frame="Generation",
        animation_group="Name",
        hover_name="Name",
        hover_data={"Type 1": True, "Type 2": True, "Legendary": True},
        color_continuous_scale="Turbo",
        range_x=[0, 195],
        range_y=[0, 240],
        range_z=[0, 190],
        range_color=[180, 780]
    )

    fig.update_layout(
        title="4D Hyper-Dimensional Stat Evolution (Dimensions: Atk x Def x Spd + HP Size + Total Color + Gen Time)",
        scene=dict(
            xaxis=dict(title="Attack", backgroundcolor="#0b132b", gridcolor="rgba(255,255,255,0.1)", showbackground=True),
            yaxis=dict(title="Defense", backgroundcolor="#0b132b", gridcolor="rgba(255,255,255,0.1)", showbackground=True),
            zaxis=dict(title="Speed", backgroundcolor="#0b132b", gridcolor="rgba(255,255,255,0.1)", showbackground=True),
            camera=dict(eye=dict(x=1.7, y=1.7, z=1.2))
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#f8fafc", family="Inter, sans-serif"),
        height=650,
        margin=dict(l=10, r=10, t=40, b=10)
    )
    return fig

def build_4d_battle_trajectory(trajectory, p1_name, p2_name):
    """
    Builds an interactive 3D/4D battle dynamic trajectory in stat space:
    Animates the turn-by-turn health drain, combat vectors, and clash positions.
    """
    df_traj = pd.DataFrame(trajectory)
    
    fig = go.Figure()

    # P1 Path in 3D (X: Attack, Y: Defense, Z: Current HP)
    fig.add_trace(go.Scatter3d(
        x=df_traj["p1_x"],
        y=df_traj["p1_y"],
        z=df_traj["p1_hp"],
        mode="lines+markers",
        name=f"{p1_name} Trajectory",
        line=dict(color="#38bdf8", width=6),
        marker=dict(size=8, color="#38bdf8", symbol="circle"),
        hovertext=[f"Turn {r['turn']}: {p1_name} HP {r['p1_hp']} ({r['p1_hp_pct']}%)" for _, r in df_traj.iterrows()],
        hoverinfo="text"
    ))

    # P2 Path in 3D
    fig.add_trace(go.Scatter3d(
        x=df_traj["p2_x"],
        y=df_traj["p2_y"],
        z=df_traj["p2_hp"],
        mode="lines+markers",
        name=f"{p2_name} Trajectory",
        line=dict(color="#f43f5e", width=6),
        marker=dict(size=8, color="#f43f5e", symbol="diamond"),
        hovertext=[f"Turn {r['turn']}: {p2_name} HP {r['p2_hp']} ({r['p2_hp_pct']}%)" for _, r in df_traj.iterrows()],
        hoverinfo="text"
    ))

    # Add clash midpoint connecting lines
    for _, row in df_traj.iterrows():
        fig.add_trace(go.Scatter3d(
            x=[row["p1_x"], row["p2_x"]],
            y=[row["p1_y"], row["p2_y"]],
            z=[row["p1_hp"], row["p2_hp"]],
            mode="lines",
            line=dict(color="rgba(255,255,255,0.25)", width=2, dash="dot"),
            showlegend=False,
            hoverinfo="skip"
        ))

    fig.update_layout(
        title=f"4D Battle Phase Trajectory: {p1_name} vs {p2_name}",
        scene=dict(
            xaxis=dict(title="Physical Attack Power", backgroundcolor="#0f172a", gridcolor="rgba(255,255,255,0.1)"),
            yaxis=dict(title="Physical Defense Resilience", backgroundcolor="#0f172a", gridcolor="rgba(255,255,255,0.1)"),
            zaxis=dict(title="Remaining HP (Health Drain Axis)", backgroundcolor="#0f172a", gridcolor="rgba(255,255,255,0.1)"),
            camera=dict(eye=dict(x=1.6, y=1.6, z=1.3))
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#f8fafc", family="Inter, sans-serif"),
        height=580,
        margin=dict(l=10, r=10, t=40, b=10)
    )
    return fig
