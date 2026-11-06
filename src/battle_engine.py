import random
from .data_loader import get_type_multiplier

def simulate_battle(p1, p2, max_turns=15, seed=42):
    """
    Simulates a turn-based battle between two Pokémon.
    Records turn-by-turn states for 4D animation (X, Y, Z, Time, HP).
    """
    random.seed(seed)
    
    # Extract stats
    p1_stats = {
        "name": p1["Name"],
        "max_hp": p1["HP"],
        "hp": p1["HP"],
        "atk": p1["Attack"],
        "dfn": p1["Defense"],
        "sp_atk": p1["Sp. Atk"],
        "sp_dfn": p1["Sp. Def"],
        "speed": p1["Speed"],
        "type1": p1["Type 1"],
        "type2": p1["Type 2"],
        "sprite": p1.get("Sprite_URL", "")
    }
    
    p2_stats = {
        "name": p2["Name"],
        "max_hp": p2["HP"],
        "hp": p2["HP"],
        "atk": p2["Attack"],
        "dfn": p2["Defense"],
        "sp_atk": p2["Sp. Atk"],
        "sp_dfn": p2["Sp. Def"],
        "speed": p2["Speed"],
        "type1": p2["Type 1"],
        "type2": p2["Type 2"],
        "sprite": p2.get("Sprite_URL", "")
    }
    
    trajectory = []
    combat_log = []
    
    # Initial state (turn 0)
    trajectory.append({
        "turn": 0,
        "p1_name": p1_stats["name"],
        "p1_hp_pct": 100.0,
        "p1_hp": p1_stats["hp"],
        "p1_x": p1_stats["atk"],
        "p1_y": p1_stats["dfn"],
        "p1_z": p1_stats["hp"],
        "p2_name": p2_stats["name"],
        "p2_hp_pct": 100.0,
        "p2_hp": p2_stats["hp"],
        "p2_x": p2_stats["atk"],
        "p2_y": p2_stats["dfn"],
        "p2_z": p2_stats["hp"],
        "action": "Battle Commencing!"
    })
    
    turn = 1
    winner = None
    
    while turn <= max_turns and p1_stats["hp"] > 0 and p2_stats["hp"] > 0:
        # Determine priority by Speed (with small random factor for speed ties)
        p1_first = (p1_stats["speed"] + random.uniform(-2, 2)) >= (p2_stats["speed"] + random.uniform(-2, 2))
        first, second = (p1_stats, p2_stats) if p1_first else (p2_stats, p1_stats)
        
        # Action 1: First strikes second
        mult1 = get_type_multiplier(first["type1"], second["type1"], second["type2"])
        # Standard Pokémon damage formula approx: ((2 * Level / 5 + 2) * Power * A / D) / 50 + 2
        raw_damage1 = max(5, int(((first["atk"] * 1.4) / max(1, second["dfn"])) * 28 * mult1 * random.uniform(0.85, 1.0)))
        second["hp"] = max(0, second["hp"] - raw_damage1)
        
        eff_desc = "Super effective!" if mult1 > 1.0 else ("Not very effective..." if mult1 < 1.0 and mult1 > 0 else ("No effect!" if mult1 == 0 else "Normal strike."))
        combat_log.append(f"Turn {turn} (Strike A): {first['name']} attacked {second['name']} for {raw_damage1} DMG! ({eff_desc})")
        
        if second["hp"] == 0:
            winner = first["name"]
            trajectory.append({
                "turn": turn,
                "p1_name": p1_stats["name"],
                "p1_hp_pct": round(max(0, p1_stats["hp"] / p1_stats["max_hp"]) * 100, 1),
                "p1_hp": p1_stats["hp"],
                "p1_x": p1_stats["atk"],
                "p1_y": p1_stats["dfn"],
                "p1_z": p1_stats["hp"],
                "p2_name": p2_stats["name"],
                "p2_hp_pct": round(max(0, p2_stats["hp"] / p2_stats["max_hp"]) * 100, 1),
                "p2_hp": p2_stats["hp"],
                "p2_x": p2_stats["atk"],
                "p2_y": p2_stats["dfn"],
                "p2_z": p2_stats["hp"],
                "action": f"{first['name']} landed a finishing blow!"
            })
            break
            
        # Action 2: Second counter-attacks
        mult2 = get_type_multiplier(second["type1"], first["type1"], first["type2"])
        raw_damage2 = max(5, int(((second["atk"] * 1.4) / max(1, first["dfn"])) * 28 * mult2 * random.uniform(0.85, 1.0)))
        first["hp"] = max(0, first["hp"] - raw_damage2)
        
        eff_desc2 = "Super effective!" if mult2 > 1.0 else ("Not very effective..." if mult2 < 1.0 and mult2 > 0 else ("No effect!" if mult2 == 0 else "Normal strike."))
        combat_log.append(f"Turn {turn} (Strike B): {second['name']} retaliated against {first['name']} for {raw_damage2} DMG! ({eff_desc2})")
        
        if first["hp"] == 0:
            winner = second["name"]
            
        trajectory.append({
            "turn": turn,
            "p1_name": p1_stats["name"],
            "p1_hp_pct": round(max(0, p1_stats["hp"] / p1_stats["max_hp"]) * 100, 1),
            "p1_hp": p1_stats["hp"],
            "p1_x": p1_stats["atk"],
            "p1_y": p1_stats["dfn"],
            "p1_z": p1_stats["hp"],
            "p2_name": p2_stats["name"],
            "p2_hp_pct": round(max(0, p2_stats["hp"] / p2_stats["max_hp"]) * 100, 1),
            "p2_hp": p2_stats["hp"],
            "p2_x": p2_stats["atk"],
            "p2_y": p2_stats["dfn"],
            "p2_z": p2_stats["hp"],
            "action": f"Turn {turn} concluded: {first['name']} HP: {first['hp']} | {second['name']} HP: {second['hp']}"
        })
        
        turn += 1
        
    if not winner:
        winner = p1_stats["name"] if p1_stats["hp"] >= p2_stats["hp"] else p2_stats["name"]
        
    return {
        "winner": winner,
        "turns": turn - 1 if turn > 1 else 1,
        "trajectory": trajectory,
        "combat_log": combat_log,
        "p1_final": p1_stats,
        "p2_final": p2_stats
    }
