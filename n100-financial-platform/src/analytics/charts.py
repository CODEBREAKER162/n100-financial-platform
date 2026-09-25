import os
import numpy as np
import matplotlib.pyplot as plt

def generate_radar_chart(company_name: str, peer_group: str, metrics: list, company_values: list, peer_avg_values: list, output_dir: str = "reports/radar_charts"):
    """Generates an 8-axis polar radar chart for a company vs its peer group average."""
    os.makedirs(output_dir, exist_ok=True)
    
    num_vars = len(metrics)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    
    # Complete the loop for polar plot
    company_values = company_values + [company_values[0]]
    peer_avg_values = peer_avg_values + [peer_avg_values[0]]
    angles += angles[:1]
    
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    
    # Peer group average (Dashed line)
    ax.plot(angles, peer_avg_values, color='gray', linewidth=1.5, linestyle='--', label=f'{peer_group} Avg')
    ax.fill(angles, peer_avg_values, color='gray', alpha=0.1)
    
    # Company values (Solid filled polygon)
    ax.plot(angles, company_values, color='#1f77b4', linewidth=2, label=company_name)
    ax.fill(angles, company_values, color='#1f77b4', alpha=0.25)
    
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(metrics, fontsize=9)
    ax.set_yticklabels([])
    plt.title(f"{company_name} - Peer Comparison", size=13, y=1.08)
    plt.legend(loc='upper right', bbox_to_anchor=(1.2, 1.1))
    
    clean_name = "".join(c for c in company_name if c.isalnum() or c in (' ', '_')).rstrip()
    filepath = os.path.join(output_dir, f"{clean_name}_radar.png")
    plt.savefig(filepath, bbox_inches='tight')
    plt.close()
    return filepath
