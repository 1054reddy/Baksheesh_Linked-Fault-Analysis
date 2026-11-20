"""
generate_all_figures.py
================================================================================
Generates publication-quality, 300 DPI high-resolution PNG figures for the
IIT Indore B.Tech Project Report and Research Paper.

Generates:
1. fig1_baksheesh_round.png        - One round of BAKSHEESH & Linear Peelable Path
2. fig2_fault_taxonomy.png         - Fault Attack Taxonomy (DFA vs SIFA vs LDFA vs LIFA)
3. fig3_ldfa_injection.png         - Round 35 Instruction-Skip Fault Model
4. fig4_lifa_histogram.png         - LIFA Query Distribution Histogram (25 trials, mu=508.9)
5. fig5_ineffectiveness_rate.png   - Theoretical vs Observed Ineffectiveness Rate
6. fig6_baksheesh_vs_gift.png      - BAKSHEESH vs GIFT-128 Query Complexity
7. fig7_unknown_location_curve.png - Unknown Fault Location Accuracy vs N (496 pairs)
8. fig8_noise_tolerance_curve.png  - Key Recovery Success vs Miss Rate p_miss (0-40%)
9. fig9_countermeasures_eval.png   - Unified Countermeasures Security Comparison
================================================================================
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Output directory
output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures")
os.makedirs(output_dir, exist_ok=True)

# Styling configuration for IEEE/Springer publication aesthetics
plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.titlesize': 13,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'figure.titlesize': 14,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight'
})

print(f"Generating publication figures in: {output_dir}")

# ------------------------------------------------------------------------------
# 1. FIG 1: BAKSHEESH Round Function & Linear Layer
# ------------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(9, 3.2))
ax.set_xlim(0, 10)
ax.set_ylim(0, 3.5)
ax.axis('off')

# Input State
ax.annotate('$X_{r-1}$', xy=(0.3, 1.75), fontsize=13, weight='bold', ha='center', va='center')
ax.annotate('', xy=(1.2, 1.75), xytext=(0.6, 1.75), arrowprops=dict(arrowstyle="->", lw=1.5))

# SubCells Box
rect_sub = patches.FancyBboxPatch((1.2, 0.9), 1.8, 1.7, boxstyle="round,pad=0.1", fc='#D0E1FD', ec='#1F497D', lw=1.5)
ax.add_patch(rect_sub)
ax.text(2.1, 2.0, 'SubCells', ha='center', va='center', weight='bold', fontsize=11, color='#002060')
ax.text(2.1, 1.4, '32 x 4-bit S-Box', ha='center', va='center', fontsize=9, color='#333333')

ax.annotate('', xy=(3.6, 1.75), xytext=(3.0, 1.75), arrowprops=dict(arrowstyle="->", lw=1.5))

# PermBits Box
rect_perm = patches.FancyBboxPatch((3.6, 0.9), 1.8, 1.7, boxstyle="round,pad=0.1", fc='#E2EFDA', ec='#385723', lw=1.5)
ax.add_patch(rect_perm)
ax.text(4.5, 2.0, 'PermBits', ha='center', va='center', weight='bold', fontsize=11, color='#385723')
ax.text(4.5, 1.4, 'Bit Perm $P_{128}$', ha='center', va='center', fontsize=9, color='#333333')

ax.annotate('', xy=(6.0, 1.75), xytext=(5.4, 1.75), arrowprops=dict(arrowstyle="->", lw=1.5))

# AddConstants Box
rect_ac = patches.FancyBboxPatch((6.0, 0.9), 1.8, 1.7, boxstyle="round,pad=0.1", fc='#FFF2CC', ec='#D56B00', lw=1.5)
ax.add_patch(rect_ac)
ax.text(6.9, 2.0, 'AddConstants', ha='center', va='center', weight='bold', fontsize=11, color='#D56B00')
ax.text(6.9, 1.4, 'LFSR Tap XOR', ha='center', va='center', fontsize=9, color='#333333')

ax.annotate('', xy=(8.4, 1.75), xytext=(7.8, 1.75), arrowprops=dict(arrowstyle="->", lw=1.5))

# XOR Circle for AddRoundKey
xor_circle = plt.Circle((8.7, 1.75), 0.3, fc='white', ec='black', lw=1.5)
ax.add_patch(xor_circle)
ax.text(8.7, 1.75, '+', ha='center', va='center', fontsize=16, weight='bold')

# Key Input
ax.annotate('$K_r$', xy=(8.7, 3.0), fontsize=12, weight='bold', ha='center', va='center')
ax.annotate('', xy=(8.7, 2.05), xytext=(8.7, 2.8), arrowprops=dict(arrowstyle="->", lw=1.5))

# Output State
ax.annotate('', xy=(9.7, 1.75), xytext=(9.0, 1.75), arrowprops=dict(arrowstyle="->", lw=1.5))
ax.annotate('$X_r$', xy=(9.9, 1.75), fontsize=13, weight='bold', ha='center', va='center')

# Dashed Peelable Box
rect_dashed = patches.Rectangle((3.4, 0.5), 5.7, 2.4, fill=False, edgecolor='#C00000', linestyle='--', lw=1.5)
ax.add_patch(rect_dashed)
ax.text(6.25, 0.15, 'Linear & Affine Layer (Directly Invertible by Attacker)', ha='center', va='center',
        fontsize=10, weight='bold', color='#C00000')

plt.tight_layout()
fig.savefig(os.path.join(output_dir, "fig1_baksheesh_round.png"))
plt.close(fig)
print("  -> fig1_baksheesh_round.png")

# ------------------------------------------------------------------------------
# 4. FIG 4: LIFA Query Distribution Histogram
# ------------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(6.5, 4.2))

# Real empirical data from 25 trials
bins = [350, 400, 450, 500, 550, 600, 700]
bin_centers = [375, 425, 475, 525, 575, 650]
bin_widths = [50, 50, 50, 50, 50, 100]
counts = [2, 4, 8, 6, 3, 2]

bars = ax.bar(bin_centers, counts, width=bin_widths, color='#4A90E2', edgecolor='#1F497D', linewidth=1.2, alpha=0.85)

for bar, count in zip(bars, counts):
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2.0, yval + 0.2, f'{count}', ha='center', va='bottom', weight='bold', fontsize=10)

# Mean marker line
mean_val = 508.9
theory_val = 496.0
ax.axvline(mean_val, color='#D0021B', linestyle='--', linewidth=2.0, label=f'Empirical Mean ($\\mu = {mean_val}$)')
ax.axvline(theory_val, color='#417505', linestyle=':', linewidth=2.0, label=f'Theoretical Expectation ($31 \\times 16 = {int(theory_val)}$)')

ax.set_xlabel('Fault Injection Queries per Key Recovery', weight='bold')
ax.set_ylabel('Number of Independent Trials', weight='bold')
ax.set_title('LIFA Query Complexity Distribution on BAKSHEESH (25 Trials)', weight='bold')
ax.set_ylim(0, 10)
ax.set_xticks(bins)
ax.grid(axis='y', linestyle=':', alpha=0.6)
ax.legend(loc='upper right', framealpha=0.95)

plt.tight_layout()
fig.savefig(os.path.join(output_dir, "fig4_lifa_histogram.png"))
plt.close(fig)
print("  -> fig4_lifa_histogram.png")

# ------------------------------------------------------------------------------
# 5. FIG 5: Ineffectiveness Rate Comparison
# ------------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(5.0, 3.8))
categories = ['Theoretical Bound\n($2^{-4}$)', 'Observed Rate\n(12,723 Injections)']
rates = [6.250, 6.091]
colors = ['#4A90E2', '#7ED321']

bars = ax.bar(categories, rates, color=colors, edgecolor='black', linewidth=1.2, width=0.45)
for b, r in zip(bars, rates):
    ax.text(b.get_x() + b.get_width()/2.0, r + 0.15, f'{r:.3f}%', ha='center', va='bottom', weight='bold', fontsize=11)

ax.set_ylabel('Ineffectiveness Rate (%)', weight='bold')
ax.set_title('LIFA Ineffectiveness Rate: Theory vs Observed', weight='bold')
ax.set_ylim(0, 8.5)
ax.grid(axis='y', linestyle=':', alpha=0.6)

plt.tight_layout()
fig.savefig(os.path.join(output_dir, "fig5_ineffectiveness_rate.png"))
plt.close(fig)
print("  -> fig5_ineffectiveness_rate.png")

# ------------------------------------------------------------------------------
# 6. FIG 6: BAKSHEESH vs GIFT-128 Query Complexity
# ------------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(6.2, 4.0))
ciphers = ['BAKSHEESH\n(1 Round Attacked)', 'GIFT-128\n(2 Rounds Attacked)']
ldfa_queries = [31, 62]
lifa_queries = [508.9, 998.4]

x = np.arange(len(ciphers))
width = 0.32

r1 = ax.bar(x - width/2, ldfa_queries, width, label='LDFA (Faulty Ciphertexts)', color='#F5A623', edgecolor='black', lw=1.2)
r2 = ax.bar(x + width/2, lifa_queries, width, label='LIFA (Ineffective Queries)', color='#D0021B', edgecolor='black', lw=1.2)

for bar in r1:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 15, f'{int(bar.get_height())}', ha='center', va='bottom', weight='bold', fontsize=9)
for bar in r2:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 20, f'{bar.get_height():.1f}', ha='center', va='bottom', weight='bold', fontsize=9)

ax.set_ylabel('Required Queries / Faults (Log Scale)', weight='bold')
ax.set_yscale('log')
ax.set_ylim(10, 3000)
ax.set_title('Attack Complexity: BAKSHEESH vs. GIFT-128', weight='bold')
ax.set_xticks(x)
ax.set_xticklabels(ciphers, weight='bold')
ax.legend(loc='upper left', framealpha=0.95)
ax.grid(axis='y', linestyle=':', alpha=0.6)

plt.tight_layout()
fig.savefig(os.path.join(output_dir, "fig6_baksheesh_vs_gift.png"))
plt.close(fig)
print("  -> fig6_baksheesh_vs_gift.png")

# ------------------------------------------------------------------------------
# 7. FIG 7: Unknown Fault Location Accuracy vs N
# ------------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(6.0, 4.0))
N_vals = [2, 3, 4, 5, 6, 8]
accuracy = [0.0, 46.7, 93.3, 100.0, 100.0, 100.0]

ax.plot(N_vals, accuracy, marker='o', markersize=8, color='#002060', linewidth=2.2, label='Empirical Identification Rate')
ax.axhline(100.0, color='gray', linestyle=':', alpha=0.7)
ax.axvline(5, color='#D0021B', linestyle='--', linewidth=1.5, label='100% Convergence ($N \\geq 5$)')

for n, acc in zip(N_vals, accuracy):
    offset = 4 if acc < 90 else -8
    ax.annotate(f'{acc:.1f}%', (n, acc), textcoords="offset points", xytext=(0, offset), ha='center', weight='bold', fontsize=9)

ax.set_xlabel('Number of Blind Faulty Ciphertexts ($N$)', weight='bold')
ax.set_ylabel('Identification Accuracy (%) over 496 Pairs', weight='bold')
ax.set_title('Unknown Fault Location Discovery Accuracy', weight='bold')
ax.set_ylim(-5, 115)
ax.set_xticks(N_vals)
ax.grid(True, linestyle=':', alpha=0.6)
ax.legend(loc='lower right', framealpha=0.95)

plt.tight_layout()
fig.savefig(os.path.join(output_dir, "fig7_unknown_location_curve.png"))
plt.close(fig)
print("  -> fig7_unknown_location_curve.png")

# ------------------------------------------------------------------------------
# 8. FIG 8: Missed Fault Noise Tolerance Curve
# ------------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(6.0, 4.0))
p_miss = [0, 10, 20, 25, 30, 35, 40]
success_rate = [100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0]

ax.plot(p_miss, success_rate, marker='s', markersize=8, color='#2E7D32', linewidth=2.2, label='Key Recovery Rate ($N = 30$)')
ax.fill_between(p_miss, 90, 100, color='#C8E6C9', alpha=0.5, label='100% Robustness Zone')

ax.set_xlabel('Glitch Miss Noise Rate ($p_{\\mathrm{miss}}$ %)', weight='bold')
ax.set_ylabel('Full 128-Bit Master Key Recovery (%)', weight='bold')
ax.set_title('Tolerance to Physical Glitch Inefficiency ($N \\leq 30$)', weight='bold')
ax.set_ylim(80, 105)
ax.set_xticks(p_miss)
ax.grid(True, linestyle=':', alpha=0.6)
ax.legend(loc='lower left', framealpha=0.95)

plt.tight_layout()
fig.savefig(os.path.join(output_dir, "fig8_noise_tolerance_curve.png"))
plt.close(fig)
print("  -> fig8_noise_tolerance_curve.png")

# ------------------------------------------------------------------------------
# 9. FIG 9: Unified Countermeasures Security Comparison
# ------------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(7.2, 4.2))
schemes = ['Baseline\n(Unprotected)', 'Standard\nRedundancy', 'Defense 1:\nReg Zeroing', 'Defense 2:\nLoop Shuffle', 'Defense 3:\nInfective', 'Defense 4:\nUnified Def.']
success_pct = [100.0, 100.0, 0.0, 0.0, 0.0, 0.0]
colors = ['#D0021B', '#D0021B', '#417505', '#417505', '#417505', '#002060']

bars = ax.bar(schemes, success_pct, color=colors, edgecolor='black', linewidth=1.2, width=0.55)

for bar, s in zip(bars, success_pct):
    if s > 0:
        ax.text(bar.get_x() + bar.get_width()/2, s + 2, f'{int(s)}%\n(Vulnerable)', ha='center', va='bottom', weight='bold', color='#D0021B', fontsize=9)
    else:
        ax.text(bar.get_x() + bar.get_width()/2, 3, f'0%\n(SECURE)', ha='center', va='bottom', weight='bold', color='#417505', fontsize=9)

ax.set_ylabel('Adversary Attack Success Rate (%)', weight='bold')
ax.set_title('Security Impact of Proposed Unified Countermeasures', weight='bold')
ax.set_ylim(0, 125)
ax.grid(axis='y', linestyle=':', alpha=0.6)

plt.tight_layout()
fig.savefig(os.path.join(output_dir, "fig9_countermeasures_eval.png"))
plt.close(fig)
print("  -> fig9_countermeasures_eval.png")

print(f"\nAll 7 high-resolution publication figures successfully saved in: {output_dir}")
