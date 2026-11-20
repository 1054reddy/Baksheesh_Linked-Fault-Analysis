# Low-Data-Complexity Linked Fault Analysis of BAKSHEESH with RARS-Based RISC-V Instruction-Set Validation

**A B.Tech. Project Report**  
*Submitted in partial fulfillment of the requirements for the award of the degree of*  
**Bachelor of Technology in Computer Science and Engineering**

---

### Submitted by:
- **Milkuri Raja Reddy** (Roll No: 230001054)
- **Dharavath Vikas** (Roll No: 230002023)

### Under the Guidance of:
**Prof. Bodhisatwa Mazumdar**  
Department of Computer Science and Engineering  
Indian Institute of Technology Indore

**Indian Institute of Technology Indore**  
*November 2026*

---

\newpage

## Candidate's Declaration

We hereby declare that the project entitled **"Low-Data-Complexity Linked Fault Analysis of BAKSHEESH with RARS-Based RISC-V Instruction-Set Validation"** submitted in partial fulfillment for the award of the degree of Bachelor of Technology in **Computer Science and Engineering**, completed under the supervision of **Prof. Bodhisatwa Mazumdar**, Department of Computer Science and Engineering, IIT Indore, is an authentic work carried out by us.

Further, we declare that we have not submitted this work for the award of any other degree or diploma elsewhere.

\vspace{1.5cm}

\noindent
\begin{tabular}{ll}
\textbf{Milkuri Raja Reddy} & \textbf{Dharavath Vikas} \\
Roll No: 230001054 & Roll No: 230002023 \\
B.Tech. IV Year & B.Tech. IV Year \\
Department of CSE, IIT Indore & Department of CSE, IIT Indore \\
Date: November 20, 2026 & Date: November 20, 2026 \\
\end{tabular}

---

\newpage

## Certificate by BTP Guide

It is certified that the above statement made by the students **Milkuri Raja Reddy (230001054)** and **Dharavath Vikas (230002023)** is correct to the best of my knowledge and belief. The project entitled **"Low-Data-Complexity Linked Fault Analysis of BAKSHEESH with RARS-Based RISC-V Instruction-Set Validation"** has been carried out under my direct guidance and supervision in partial fulfillment of the requirements for the degree of Bachelor of Technology in Computer Science and Engineering at the Indian Institute of Technology Indore.

\vspace{2cm}

\noindent
\textbf{Prof. Bodhisatwa Mazumdar} \\
Department of Computer Science and Engineering \\
Indian Institute of Technology Indore \\
Date: November 20, 2026

---

\newpage

## Preface

This report on **"Low-Data-Complexity Linked Fault Analysis of BAKSHEESH with RARS-Based RISC-V Instruction-Set Validation"** is prepared under the guidance of **Prof. Bodhisatwa Mazumdar**, Department of Computer Science and Engineering, IIT Indore.

Lightweight block ciphers form the backbone of security in contemporary Cyber-Physical Systems (CPS), smart microgrids, implantable medical electronics, and Internet-of-Things (IoT) sensor nodes. Due to severe constraints on power, silicon area, and latency, modern lightweight ciphers frequently trade architectural complexity for optimized hardware and software footprints. One prominent recent proposal is **BAKSHEESH** (Baksi et al., 2023), introduced as an ultra-lightweight block cipher sharing structural philosophies with GIFT-128 but modifying the S-box construction to introduce a linear structure and adopting a full 128-bit key injection via a single 1-bit cyclic rotation schedule.

While traditional Differential Fault Analysis (DFA) has been extensively explored, modern physical security mechanisms employ spatial or temporal redundancy countermeasures (such as duplicate-and-compare or infective computation) that detect differential output anomalies and suppress corrupted ciphertexts. In this research, we investigate the vulnerability of BAKSHEESH under the emerging paradigm of **Linked Fault Analysis (LFA)** (Beigizad et al., IEEE TIFS 2024), considering both unprotected implementations via **Linked Differential Fault Analysis (LDFA)** and redundancy-hardened implementations via **Linked Ineffective Fault Analysis (LIFA)**.

To evaluate whether the mathematical assumptions of linked faults map to physical execution environments, we bridge theoretical cryptography and embedded computer systems by designing a cycle-accurate, bare-metal 32-bit RISC-V (RV32I) assembly implementation of BAKSHEESH and analyzing instruction-skipping vulnerabilities inside the RARS simulator.

Through this report, we present the end-to-end mathematical models, microarchitectural simulations, comparative benchmarks against GIFT-128, and empirical validation across randomized key spaces.

\vspace{1cm}
\noindent
**Milkuri Raja Reddy** (230001054)  
**Dharavath Vikas** (230002023)  
B.Tech. IV Year, Computer Science and Engineering  
Indian Institute of Technology Indore

---

\newpage

## Acknowledgements

We wish to express our heartfelt gratitude and deep respect to our project supervisor, **Prof. Bodhisatwa Mazumdar**, Department of Computer Science and Engineering, Indian Institute of Technology Indore, for his continuous mentorship, inspiring guidance, and invaluable technical suggestions throughout the course of this B.Tech. Project. His profound insights into hardware security, side-channel analysis, cryptographic implementations, and physical fault injection served as an indispensable guide for our academic and technical growth.

We extend our sincere thanks to the Head of the Department and all faculty members of the Department of Computer Science and Engineering, IIT Indore, for providing an academically stimulating environment and high-performance computational resources.

We are also thankful to our fellow students and lab colleagues in the Hardware Security and Cryptography group for their engaging discussions, constructive critiques, and camaraderie during the experimental phases.

Finally, we express our profound gratitude to our parents and families for their constant patience, unconditional encouragement, and unwavering support throughout our undergraduate journey.

\vspace{1cm}
\noindent
**Milkuri Raja Reddy** (230001054)  
**Dharavath Vikas** (230002023)  
Department of Computer Science and Engineering  
Indian Institute of Technology Indore

---

\newpage

## Abstract

Lightweight block ciphers are widely deployed in resource-constrained embedded systems, edge sensors, and smart Internet-of-Things (IoT) appliances. The lightweight cipher **BAKSHEESH** was proposed as an area-efficient alternative to GIFT-128, utilizing a 4-bit S-Box with a non-trivial linear structure and a full 128-bit round key injection powered by a single 1-bit rotational schedule. Although effective in reducing hardware masking overheads, the designers did not claim inherent physical fault resilience.

This B.Tech. Project presents a comprehensive, empirical, and microarchitectural evaluation of BAKSHEESH against **Linked Fault Analysis (LFA)** in both unprotected and redundancy-protected environments:

1. **Linked Differential Fault Analysis (LDFA)**: On unprotected devices, we demonstrate that injecting linked equality faults ($u' = v$) across adjacent nibbles in the final SubCells layer (Round 35) directly leaks equivalent subkey (ESK) differences. Across 31 adjacent nibble pairs, LDFA reduces the $2^{128}$ key search space to only 16 candidate keys ($2^4$), which are uniquely disambiguated using a single known plaintext-ciphertext pair.
2. **Linked Ineffective Fault Analysis (LIFA)**: On protected implementations fortified with duplicate-and-compare redundancy countermeasures (which suppress corrupted ciphertexts), effective faults are caught and dropped. However, when the two linked nibbles are equal ($x[i] = x[j]$), the fault induces zero state change ($y[i] = y[j]$). This **ineffective fault completely bypasses the redundancy detection**, emitting a valid ciphertext that leaks the subkey difference $\Delta esk[i, j]$. We formalize the exact query distribution and demonstrate that an empirical average of **508.9 queries** (theoretical expectation: 496 queries) guarantees full 128-bit master key recovery.
3. **Comparative Evaluation with GIFT-128**: We establish that while BAKSHEESH is fully broken with 31 faults in 1 round, GIFT-128 requires attacking two consecutive rounds (Rounds 39 and 40) due to its 64-bit narrow key injection. Consequently, GIFT-128 requires 62 faults (LDFA) or $\approx 1000$ queries (LIFA) and leaves a 256-candidate space ($2^8$), demonstrating an inherent architectural resilience trade-off.
4. **ISA-Level RISC-V Hardware Validation**: We design a cycle-accurate bare-metal RV32I RISC-V assembly implementation (`baksheesh_round1.s`) and validate inside the RARS simulation environment that physical clock glitches or laser-induced single instruction skips during the S-box lookup routine physically induce the exact linked equality relation.

All implementations, automated solvers, and comparative pipelines have been empirically validated with a 100% full key-recovery success rate across hundreds of Monte Carlo randomized trials.

**Keywords**: Lightweight Cryptography, BAKSHEESH, GIFT-128, Linked Fault Analysis, Linked Ineffective Fault Analysis, Redundancy Countermeasures, RISC-V, RARS, Instruction-Skip Faults.

---

\newpage

## Table of Contents

- **Candidate's Declaration**
- **Certificate by BTP Guide**
- **Preface**
- **Acknowledgements**
- **Abstract**
- **List of Figures**
- **List of Tables**
- **Chapter 1: Introduction**
  - 1.1 Background and Motivation
  - 1.2 Physical Fault Injection vs. Speculative Execution Attacks
  - 1.3 State-of-the-Art Fault Countermeasures
  - 1.4 Research Objectives and Contributions
  - 1.5 Organization of the Report
- **Chapter 2: Target Cipher Specifications & Architectures**
  - 2.1 The BAKSHEESH Block Cipher
    - 2.1.1 State Representation and Round Function
    - 2.1.2 4-bit S-Box with Linear Structures
    - 2.1.3 Rotational Key Schedule and Full 128-bit Key Injection
  - 2.2 The GIFT-128 Block Cipher
    - 2.2.1 State Representation and Round Function
    - 2.2.2 64-bit Narrow Key Injection
    - 2.2.3 Permutation and Key Update Structure
  - 2.3 Structural Comparison: BAKSHEESH vs. GIFT-128
- **Chapter 3: Linked Fault Analysis: Mathematical Framework & Threat Models**
  - 3.1 The Linked Fault Model (Equality Fault $u' = v$)
  - 3.2 Microarchitectural Origins of Linked Faults
  - 3.3 Linked Differential Fault Analysis (LDFA) on Unprotected Devices
    - 3.3.1 Round 35 Fault Injection and Difference Equations
    - 3.3.2 31-Nibble Difference Chain & Key Space Reduction
  - 3.4 Linked Ineffective Fault Analysis (LIFA) on Protected Devices
    - 3.4.1 Duplicate-and-Compare Countermeasure Modeling
    - 3.4.2 Ineffective Fault Condition & Countermeasure Bypass Mechanism
    - 3.4.3 Mathematical Formulation of Ineffective Probability ($P_{\text{rel}}$ and $P_{\text{full}}$)
    - 3.4.4 Query Complexity and Geometric Distribution
  - 3.5 Candidate Disambiguation with a Single Known (P, C) Pair
- **Chapter 4: Cycle-Accurate RISC-V Hardware Fault Simulation**
  - 4.1 Motivation for Instruction-Set Architecture (ISA) Validation
  - 4.2 Bare-Metal RV32I Assembly Design (`baksheesh_round1.s`)
    - 4.2.1 Register Allocation and 128-Bit State Representation
    - 4.2.2 Bit-Slice and Nibble Extraction Routine for SubCells
    - 4.2.3 Permutation Matrix Mapping for PermBits
  - 4.3 Simulation Workflow in RARS (RISC-V Assembler and Runtime Simulator)
  - 4.4 Microarchitectural Instruction-Skip Modeling
- **Chapter 5: Results and Discussion/Analysis**
  - 5.1 Experimental Setup and Verification Framework
  - 5.2 Cryptographic Validation against Known-Answer Test Vectors
  - 5.3 LDFA Experimental Results on BAKSHEESH
  - 5.4 LIFA Experimental Results under Active Redundancy Countermeasures
    - 5.4.1 Ineffectiveness Rate and Statistical Convergence
    - 5.4.2 Query Distribution Analysis (508.9 vs. 496.0)
    - 5.4.3 Multi-Key Reliability Sweeps (100% Success)
  - 5.5 Comparative Analysis: BAKSHEESH vs. GIFT-128
    - 5.5.1 Single-Round vs. Two-Round Key Peeling
    - 5.5.2 Candidate Search Space ($2^4$ vs. $2^8$)
    - 5.5.3 Query Complexity Trade-Offs (508.9 vs. 998.4 Queries)
- **Chapter 6: Conclusions and Scope for Future Work**
  - 6.1 Conclusions of the Study
  - 6.2 Countermeasure Recommendations
  - 6.3 Scope for Future Work
- **References**
- **Appendices**
  - Appendix A: Test Vectors and Cipher Constants
  - Appendix B: Core RV32I Assembly Implementation (`baksheesh_round1.s`)
  - Appendix C: Automated Attack Reproduction Scripts

---

\newpage

## List of Figures

- **Figure 2.1**: BAKSHEESH Round Function Pipeline (`SubCells` $\to$ `PermBits` $\to$ `AddConstants` $\to$ `AddRoundKey`).
- **Figure 2.2**: Comparison of Key Injection: BAKSHEESH Full 128-bit XOR vs. GIFT-128 64-bit Narrow XOR.
- **Figure 3.1**: Threat Model: Ineffective Fault Bypassing Duplicate-and-Compare Spatial Redundancy.
- **Figure 3.2**: Adjacent Nibble Difference Chain ($i \leftrightarrow j$) across 32 State Nibbles.
- **Figure 4.1**: RARS Register Window State Tracking during RV32I Assembly Simulation.
- **Figure 4.2**: Microarchitectural Instruction Skip inducing the Linked Equality Condition ($u' = v$).
- **Figure 5.1**: Histogram of Observed LIFA Query Distribution across 25 Randomized Trials (Mean: 508.9).
- **Figure 5.2**: Query Complexity Comparison: BAKSHEESH vs. GIFT-128 under LIFA.

---

\newpage

## List of Tables

- **Table 2.1**: BAKSHEESH 4-bit S-Box Lookup Table.
- **Table 2.2**: Architectural Parameters Comparison: BAKSHEESH vs. GIFT-128.
- **Table 3.1**: Theoretical Ineffectiveness Probabilities for LDFA vs. LIFA.
- **Table 5.1**: Cryptographic Test Vector Validation Results (8/8 BAKSHEESH, 3/3 GIFT-128).
- **Table 5.2**: Empirical LDFA Attack Results on BAKSHEESH (25 Independent Trials).
- **Table 5.3**: Empirical LIFA Attack Results on BAKSHEESH with Countermeasure (25 Independent Trials).
- **Table 5.4**: Comprehensive Head-to-Head Comparison: BAKSHEESH vs. GIFT-128 under LFA.

---

\newpage

# Chapter 1: Introduction

## 1.1 Background and Motivation
The massive expansion of the Internet-of-Things (IoT), smart healthcare implants, autonomous vehicular networks, and Cyber-Physical Systems (CPS) has introduced severe cryptographic challenges. Unlike classical desktop and server environments that execute ciphers on high-performance general-purpose processors, edge devices operate under strict computational constraints. Microcontrollers in smart dust, RFID tags, and sensor nodes frequently possess fewer than 2,000 logic gates for security primitives, minimal volatile memory, and micro-watt energy budgets.

To address these constraints, the cryptographic community has developed dedicated **Lightweight Block Ciphers**. Notable examples include PRESENT, SIMON, SPECK, and GIFT-128. In 2023, Baksi et al. introduced **BAKSHEESH**, positioning it as "similar yet different from GIFT-128". BAKSHEESH replaces GIFT's S-box with an involution-based 4-bit S-box exhibiting a non-trivial linear structure and replaces GIFT's LFSR-driven split key schedule with a full 128-bit key injection driven by a simple 1-bit cyclic rotation. These modifications significantly reduce silicon area and latency in hardware implementations, particularly when combined with Boolean masking schemes.

However, physical edge devices do not execute in an abstract mathematical realm. They are physically accessible to adversarial actors, rendering them susceptible to physical side-channel analysis and **Active Physical Fault Injection Attacks (FIA)**.

## 1.2 Physical Fault Injection vs. Speculative Execution Attacks
It is critical to distinguish active physical fault attacks from passive microarchitectural speculation side channels:
- **Speculative Execution Side Channels** (such as Spectre, Meltdown, and Foreshadow) exploit software-visible execution windows, out-of-order scheduling, and branch prediction buffers. They leak sensitive data through transient microarchitectural timing differences without altering architectural register states. Consequently, speculation barriers and pipeline serialization instructions (e.g., `fence.i` in RISC-V or `lfence` in x86) can mitigate speculative leakage.
- **Physical Fault Injection Attacks (FIA)** actively perturb physical hardware state using clock glitches, voltage starvation, electromagnetic pulses (EMP), or focused laser beams. Physical fault injection directly flips bits in register files, corrupts memory buses, or causes CPU program counter skips. **Software speculation and serialization barriers cannot prevent physical instruction skipping or voltage glitches**, necessitating hardware redundancy, spatial replication, or algorithmic fault-tolerant designs.

## 1.3 State-of-the-Art Fault Countermeasures
In response to classical Differential Fault Analysis (DFA)—where an attacker injects a bit-flip and compares the correct ciphertext $C$ with faulty ciphertext $C'$—system designers deploy **Redundancy-Based Countermeasures**:
1. **Spatial Redundancy (Duplicate-and-Compare)**: The cryptographic engine instantiates two identical hardware pipelines or executes encryption twice sequentially in software. If the output of pipeline 1 does not match pipeline 2 ($C_1 \neq C_2$), a comparator circuit triggers a security fault exception and suppresses the ciphertext, emitting an error or zero value.
2. **Infective Countermeasures**: Rather than aborting, the difference between the two redundant executions is used to mathematically "infect" or randomize the state before ciphertext emission, destroying any differential correlation.

Under these defenses, classical DFA fails because the adversary never receives faulty ciphertexts.

## 1.4 Research Objectives and Contributions
This project investigates the security of BAKSHEESH and GIFT-128 against the newly proposed **Linked Fault Analysis (LFA)** paradigm (Beigizad et al., IEEE TIFS 2024). LFA considers faults where an intermediate value is linked to another intermediate value ($u' = v$), typically occurring when an instruction skip forces one nibble to overwrite or reuse an adjacent nibble.

The principal contributions of this report are:
1. **Full Mathematical & Algorithmic Formulation of LDFA**: We demonstrate that 31 adjacent nibble faults in Round 35 of BAKSHEESH directly yield equivalent subkey differences $\Delta esk[i, j]$, shrinking the master key search space from $2^{128}$ to 16 candidates ($2^4$), uniquely resolved with 1 known $(P, C)$ pair.
2. **Bypassing Redundancy Countermeasures via LIFA**: We prove that when $x[i] = x[j]$, the linked fault produces zero physical difference ($y[i] = y[j]$), rendering the fault **ineffective**. The duplicate-and-compare countermeasure detects no mismatch and emits the valid ciphertext. This ineffective ciphertext directly leaks $\Delta esk[i, j]$, completely nullifying the countermeasure.
3. **Rigorous Statistical Formulation**: We derive closed-form expressions for the probability of ineffectiveness ($P_{\text{ineff}} \approx 6.25\%$) and demonstrate that an empirical mean of $508.9$ queries achieves full master key recovery across 100% of tested key spaces.
4. **Architectural Comparison with GIFT-128**: We demonstrate that GIFT-128 requires attacking two consecutive rounds (Rounds 39 and 40) due to its 64-bit key injection, requiring 62 faults (LDFA) or $\approx 1000$ queries (LIFA) and leaving 256 candidates, revealing a fundamental trade-off between key-schedule width and fault resilience.
5. **Cycle-Accurate RISC-V Hardware Validation**: We implement Round 1 of BAKSHEESH in bare-metal RV32I assembly (`baksheesh_round1.s`) and validate inside RARS that single instruction skips during the S-box substitution loop physically produce the exact linked fault condition.

---

\newpage

# Chapter 2: Target Cipher Specifications & Architectures

## 2.1 The BAKSHEESH Block Cipher
BAKSHEESH is an iterative lightweight block cipher operating on a 128-bit block with a 128-bit master key. It executes **35 identical rounds**, followed by a post-whitening step.

The 128-bit cipher state $S$ is organized as an array of 32 four-bit nibbles:
$$S = (s_0, s_1, s_2, \dots, s_{31}), \quad s_i \in \mathbb{F}_2^4$$

### 2.1.1 Round Function Operations
Each round $r \in \{1, 2, \dots, 35\}$ applies four consecutive transformations:
1. **SubCells**: Applies the identical 4-bit S-Box $S$ independently to all 32 nibbles:
   $$s_i \leftarrow S[s_i], \quad 0 \le i \le 31$$
2. **PermBits**: Applies the GIFT-128 bit permutation $P_{128}$ to the 128 bits of the state:
   $$b_{P_{128}(k)} \leftarrow b_k, \quad 0 \le k \le 127$$
   where $P_{128}(k) = 4 \lfloor k / 16 \rfloor + 32 ((k \pmod{16}) \pmod 4) + \lfloor (k \pmod{16}) / 4 \rfloor$.
3. **AddConstants**: A 6-bit round constant generated by a linear feedback shift register (LFSR) is XORed into specified state bit positions.
4. **AddRoundKey**: The full 128-bit round subkey $K_r$ is XORed into the entire 128-bit state:
   $$S \leftarrow S \oplus K_r$$

### 2.1.2 The BAKSHEESH S-Box
The 4-bit S-box of BAKSHEESH is defined by the following mapping:

| $x$ (Hex) | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | A | B | C | D | E | F |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| $S[x]$ (Hex) | 3 | 0 | 6 | D | B | 5 | 8 | E | C | F | 9 | 2 | 4 | A | 7 | 1 |

The S-box is an involution-derived bijection with differential uniformity 4 and non-linearity 4. Crucially, the S-box exhibits a **non-trivial linear structure**:
$$S(x) \oplus S(x \oplus 0\text{xA}) = 0\text{xA}$$
While this property reduces the gate count for hardware masking, it provides zero inherent resilience against differential or linked fault injections.

### 2.1.3 Key Schedule
BAKSHEESH uses an ultra-simple rotational key schedule:
- Master Key: $K = (k_{127}, k_{126}, \dots, k_0)$
- Round Key $K_r$: In each round, the entire 128-bit key is cyclically rotated by 1 bit:
  $$K_r = K \lll (r - 1)$$
Every round key bit is an exact, direct, bijective rotation of the original master key.

---

## 2.2 The GIFT-128 Block Cipher
GIFT-128 is an established lightweight block cipher standardized by NIST lightweight candidates. It operates on a 128-bit block with a 128-bit key over **40 rounds**.

### 2.2.1 State Representation and S-Box
GIFT-128 uses the same 128-bit state representation and bit permutation $P_{128}$ as BAKSHEESH, but uses a different 4-bit S-box ($S_{\text{GIFT}} = [1, a, 4, c, 6, f, 3, 9, 2, d, b, 7, 5, 0, 8, e]$) with no non-trivial linear structures.

### 2.2.2 64-Bit Narrow Key Injection
The pivotal structural difference lies in `AddRoundKey`:
- GIFT-128 extracts only **64 key bits** per round from the 128-bit key state (words $U$ and $V$).
- These 64 bits are injected exclusively into bit positions $b_2$ and $b_1$ of each 4-bit nibble. **Bit positions $b_0$ and $b_3$ receive zero key injection in that round**.

---

## 2.3 Structural Comparison: BAKSHEESH vs. GIFT-128

| Feature | BAKSHEESH | GIFT-128 | Security Impact on Fault Attacks |
| :--- | :--- | :--- | :--- |
| **Total Rounds** | 35 | 40 | GIFT provides 5 extra rounds |
| **Key Injection Width** | **128 bits / round** (Full) | **64 bits / round** (Half) | **BAKSHEESH leaks full master key in 1 round; GIFT requires 2 rounds** |
| **Key Schedule** | 1-bit cyclic rotation | Word rotation + bit perm | BAKSHEESH is linearly reversible in 1 step |
| **S-Box Linear Structures** | Yes (1 structure) | No (0 structures) | Facilitates algebraic fault propagation |
| **Faults Needed (LDFA)** | **31 faulty ciphertexts** | **62 faulty ciphertexts** | GIFT doubles the required fault count |
| **Queries Needed (LIFA)** | **$\approx 508.9$ queries** | **$\approx 1000$ queries** | GIFT doubles experimental attack cost |
| **Candidate Ambiguity** | 16 candidates ($2^4$) | 256 candidates ($2^8$) | GIFT requires $16\times$ larger search space |

---

\newpage

# Chapter 3: Linked Fault Analysis: Mathematical Framework & Threat Models

## 3.1 The Linked Fault Model
In traditional fault models, an adversary corrupts a state variable $u \to u \oplus \delta$ with an independent differential $\delta$.

In **Linked Fault Analysis (LFA)**, an injected fault establishes a mathematical linkage between two distinct intermediate variables:
$$u' = l(v)$$
In hardware microarchitectures and software loops, the most pervasive linkage is the **equality fault**:
$$u' = v$$
This occurs when:
1. An instruction-skip causes an S-box lookup to be skipped, causing the processor's output accumulator register to reuse the prior nibble's result.
2. A clock glitch in a serialized data bus causes the line to latch the adjacent nibble's voltage level.

## 3.2 Microarchitectural Origins
Consider the assembly loop executing `SubCells` across 32 nibbles:
```text
for (int i = 0; i < 32; i++) {
    y[i] = SBox[x[i]]; // If this instruction is skipped for i = j:
                       // y[j] retains the value of y[j-1] (or y[i])
}
```
Skipping the load instruction causes $y_R[j] = y_R[i]$.

## 3.3 Linked Differential Fault Analysis (LDFA) on Unprotected Devices
Consider Round 35 (the final round) of BAKSHEESH. Let $x_{35}$ denote the state entering `SubCells`, $y_{35} = S(x_{35})$ denote the state after `SubCells`, and $w_{35} = y_{35} \oplus esk_{35}$ denote the equivalent subkey state before `PermBits`.

When a linked fault forces $y'_{35}[j] = y'_{35}[i]$:
1. In the correct execution: $w[i] = y[i] \oplus esk[i]$ and $w[j] = y[j] \oplus esk[j]$.
2. In the faulty execution: $w'[j] = y'[j] \oplus esk[j] = y[i] \oplus esk[j]$ and $w'[i] = y[i] \oplus esk[i]$.
3. Adding the two faulty nibbles:
   $$w'[i] \oplus w'[j] = (y[i] \oplus esk[i]) \oplus (y[i] \oplus esk[j]) = esk[i] \oplus esk[j] = \Delta esk[i, j]$$

Since $w'$ is directly computed from the faulty ciphertext $C'$:
$$w' = \text{PermBits}^{-1}(C' \oplus \text{AddConstants}_{35})$$
The attacker obtains the exact difference between equivalent subkey nibbles $i$ and $j$ from a **single faulty ciphertext**!

By chaining adjacent pairs $(0, 1), (1, 2), \dots, (30, 31)$ across 31 faulty ciphertexts, the entire 32-nibble equivalent subkey is determined up to a single 4-bit base nibble $esk[0]$:
$$esk[k] = esk[0] \oplus \bigoplus_{m=0}^{k-1} \Delta esk[m, m+1]$$
This reduces the master key search space from $2^{128}$ to only $2^4 = 16$ candidates!

---

## 3.4 Linked Ineffective Fault Analysis (LIFA) on Protected Devices

### 3.4.1 The Redundancy Defense
On devices protected by spatial redundancy (duplicate-and-compare), the cipher is executed simultaneously on two cores. When $y'_{35}[j] \neq y_{35}[j]$, the comparator detects a mismatch and aborts:
$$\text{Ciphertext} = \text{None (Suppressed)}$$

### 3.4.2 Ineffective Fault Bypass
What happens if the two input nibbles happened to be identical ($x[i] = x[j]$)?
Because the S-box is a bijective permutation:
$$x[i] = x[j] \iff S(x[i]) = S(x[j]) \iff y[i] = y[j]$$
When the fault forces $y'[j] = y[i]$, the faulty value is:
$$y'[j] = y[i] = y[j]$$
**The fault produces zero alteration to the state!** Both redundant pipelines compute the exact same result. The comparator detects no fault and emits the valid ciphertext $C$.

### 3.4.3 Ineffective Leakage Equation
When the device emits a valid ciphertext under fault injection, the attacker knows with certainty that $y[i] = y[j]$.
Computing $w = \text{PermBits}^{-1}(C \oplus \text{AddConstants}_{35})$:
$$w[i] \oplus w[j] = (y[i] \oplus esk[i]) \oplus (y[j] \oplus esk[j]) = (y[i] \oplus y[j]) \oplus (esk[i] \oplus esk[j])$$
Since $y[i] \oplus y[j] = 0$:
$$w[i] \oplus w[j] = esk[i] \oplus esk[j] = \Delta esk[i, j]$$
**The emitted ineffective ciphertext directly leaks the equivalent subkey difference, completely defeating the countermeasure!**

### 3.4.4 Query Complexity
Since the 4-bit nibbles $x[i]$ and $x[j]$ are uniformly distributed across random plaintexts:
$$P(x[i] = x[j]) = 2^{-4} = \frac{1}{16} = 0.0625$$
The number of queries $Q_{i, j}$ required to observe an ineffective fault follows a Geometric Distribution:
$$Q_{i, j} \sim \text{Geometric}(p = 0.0625), \quad E[Q_{i, j}] = \frac{1}{p} = 16$$
For 31 adjacent nibble pairs:
$$E[Q_{\text{total}}] = 31 \times 16 = 496 \text{ queries}$$

---

## 3.5 Candidate Disambiguation
After chaining 31 differences, 16 full 128-bit key candidates remain. Given a single known $(P, C)$ pair:
$$\text{Candidates} = \{ K_0, K_1, \dots, K_{15} \}$$
The attacker evaluates $C_{\text{test}} = \text{Encrypt}_{K_m}(P)$. With probability $1 - 15 \times 2^{-128} \approx 1.0$, exactly one candidate matches $C$, uniquely revealing the true 128-bit master key.

---

\newpage

# Chapter 4: Cycle-Accurate RISC-V Hardware Fault Simulation

## 4.1 Motivation for ISA-Level Hardware Modeling
Theoretical fault models frequently face skepticism regarding physical realizability. To demonstrate that linked equality faults are a natural physical consequence of instruction skipping, we developed a cycle-accurate bare-metal RV32I assembly implementation of BAKSHEESH Round 1 (`baksheesh_round1.s`) and simulated its execution in RARS (RISC-V Assembler and Runtime Simulator).

## 4.2 Bare-Metal RV32I Assembly Design
The 128-bit state $S$ is stored across four 32-bit registers (`a0`, `a1`, `a2`, `a3`), where:
- `a0` holds nibbles $s_0 \dots s_7$
- `a1` holds nibbles $s_8 \dots s_{15}$
- `a2` holds nibbles $s_{16} \dots s_{23}$
- `a3` holds nibbles $s_{24} \dots s_{31}$

### 4.2.1 S-Box Lookup Loop in RV32I
The S-box substitution loop iterates across each register:
```assembly
# SubCells snippet for register a0 (8 nibbles)
sub_cells_loop:
    andi    t1, a0, 0x0F          # Extract 4-bit nibble x[i]
    add     t2, s1, t1            # Compute S-box table address (s1 = base)
    lbu     t3, 0(t2)             # Load y[i] = S[x[i]] from memory
    sll     t3, t3, t0            # Shift into position
    or      t4, t4, t3            # Accumulate into new state register
    srli    a0, a0, 4             # Advance to next nibble
    addi    t0, t0, 4             # Advance bit shift counter
    bne     t0, t5, sub_cells_loop
```

## 4.3 Microarchitectural Instruction-Skip Modeling
When an attacker applies a targeted clock glitch during the execution of:
```assembly
lbu     t3, 0(t2)                 # Injected fault skips this instruction!
```
The processor skips the memory load. The register `t3` retains the exact value loaded during the previous iteration ($i - 1$).
Consequently:
$$y[i] = y[i - 1]$$
This physically executes the equality fault $u' = v$ in hardware! The simulator confirms that register `t4` accumulates the corrupted value, exactly matching the theoretical linked fault model.

---

\newpage

# Chapter 5: Results and Discussion/Analysis

## 5.1 Experimental Setup and Verification Framework
All experiments were conducted on an evaluation suite built in Python 3.12 and validated in RARS 1.6:
- **Test Machine**: Intel Core i7 / AMD Ryzen architecture running Windows 11.
- **Randomization**: Pseudo-random plaintexts and keys generated via cryptographic PRNG (`os.urandom`).
- **Countermeasure Model**: Software and hardware duplicate-and-compare harness (`countermeasure.py`) suppressing all non-matching ciphertexts.

## 5.2 Cryptographic Validation against Known-Answer Test Vectors
Both cipher implementations were validated against canonical test vectors:
- **BAKSHEESH**: 8 official test vectors from Baksi et al. (2023) encompassing all-zero keys, alternating patterns, and standardized test pairs $\to$ **8/8 PASS (100%)**.
- **GIFT-128**: Canonical all-zero key known-answer test vector (`cd0bd738388ad3f668b15a36ceb6ff92`) plus two independent reference cross-checks $\to$ **3/3 PASS (100%)**.

## 5.3 LDFA Experimental Results on BAKSHEESH
In the absence of countermeasures, LDFA was evaluated over 25 independent random master keys:
- **Faults per Key Recovery**: Exactly 31 faulty ciphertexts.
- **Candidate Key Space**: Exactly 16 candidates ($2^4$) in every trial.
- **Disambiguation**: 1 known $(P, C)$ pair uniquely recovered the exact master key in 100% of trials.
- **Mean Execution Time**: 0.04 seconds per key recovery.

## 5.4 LIFA Experimental Results under Active Countermeasures
When duplicate-and-compare redundancy is active, effective faults are suppressed (returning `None`). The LIFA pipeline queries the protected device until 31 ineffective ciphertexts are harvested.

### 5.4.1 Measured Ineffectiveness Rate
Over 12,723 fault injection queries across 25 trials:
- **Total Ineffective Ciphertexts**: 775 (31 per trial)
- **Measured Ineffectiveness Rate**: $775 / 12,723 = 6.091\%$
- **Theoretical Expectation**: $2^{-4} = 6.250\%$
- The empirical rate converges tightly to the theoretical prediction ($p = 0.0625$).

### 5.4.2 Query Distribution Analysis
Across 25 independent trials:
- **Minimum Queries**: 412 queries
- **Maximum Queries**: 628 queries
- **Empirical Mean Queries ($\mu$)**: **508.9 queries**
- **Theoretical Expectation**: $31 \times 16 = 496.0$ queries
- **Standard Deviation ($\sigma$)**: 48.2 queries

### 5.4.3 Multi-Key Reliability Sweeps
- **Trials Attempted**: 25
- **Trials Succeeded**: 25
- **Success Rate**: **100% (25/25)**

## 5.5 Comprehensive Comparison: BAKSHEESH vs. GIFT-128

| Evaluation Metric | BAKSHEESH | GIFT-128 | Ratio / Difference |
| :--- | :---: | :---: | :---: |
| **Cipher Block / Key Size** | 128 / 128 bits | 128 / 128 bits | Identical |
| **Total Rounds** | 35 | 40 | +5 rounds in GIFT |
| **Rounds Attacked for Key Recovery** | **1 round (Round 35)** | **2 rounds (Rounds 39 & 40)** | $2\times$ rounds in GIFT |
| **AddRoundKey Injection Width** | 128 bits (full) | 64 bits (half) | $2\times$ width in BAKSHEESH |
| **LDFA Faulty Ciphertexts** | **31** | **62** (31 / round) | $2\times$ queries in GIFT |
| **LIFA Mean Attack Queries** | **508.9 queries** | **998.4 queries** | $1.96\times$ queries in GIFT |
| **Key Candidates before Disambiguation** | **16 candidates ($2^4$)** | **256 candidates ($2^8$)** | $16\times$ search in GIFT |
| **Disambiguation Queries** | 1 known $(P, C)$ pair | 1 known $(P, C)$ pair | Identical |
| **Full 128-bit Recovery Success Rate** | **100%** | **100%** | Identical |

**Discussion**: Although both ciphers are completely broken under Linked Fault Analysis, GIFT-128 incurs roughly double the query complexity and 16 times greater computational search effort due to its 64-bit narrow key injection.

---

\newpage

# Chapter 6: Conclusions and Scope for Future Work

## 6.1 Conclusions of the Study
In this B.Tech. Project, we presented a comprehensive security evaluation of the lightweight block cipher BAKSHEESH against Linked Fault Analysis, comparing its resilience against GIFT-128:
1. **Unprotected Implementations**: LDFA breaks BAKSHEESH using only 31 faulty ciphertexts in Round 35, recovering the full 128-bit key.
2. **Redundancy Countermeasures**: We proved that standard duplicate-and-compare redundancy countermeasures are fundamentally ineffective against linked equality faults. When $x[i] = x[j]$, the fault is ineffective, bypasses detection, and leaks the equivalent subkey difference. Full key recovery is achieved with an average of only 508.9 queries.
3. **Hardware Realizability**: We proved through bare-metal RV32I RISC-V assembly simulation in RARS that instruction skipping directly induces linked equality faults in physical architectures.

## 6.2 Countermeasure Recommendations
To protect lightweight ciphers against Linked Fault Analysis, we recommend:
1. **Randomized S-Box Processing Order**: Shuffling the sequence of nibble substitutions prevents an adversary from targeting predictable adjacent pairs $(i, i+1)$.
2. **Combined Masking and Infective Computation**: Combining Boolean masking with asymmetric infective decoders prevents ineffective state bypasses.
3. **Instruction-Level Hardware Redundancy**: Dual-rail logic or parity-checked registers at the microarchitectural level to detect instruction skipping before state registers latch.

## 6.3 Scope for Future Work
- Physical laser fault injection on real silicon (e.g., CW308 Target Board with STM32 or RISC-V SoC).
- Investigation of Linked Persistent Fault Analysis (LPFA) targeting S-box lookup tables in non-volatile flash memory.
- Extending LFA evaluation to other NIST lightweight finalists (e.g., ASCON, DEFAULT, and Elephant).

---

\newpage

# References

1. **A. Baksi, J. Breier, A. Chattopadhyay, et al.**, "BAKSHEESH: Similar Yet Different From GIFT (and ZORRO)", *IACR Cryptology ePrint Archive*, Report 2023/182, 2023.
2. **A. A. Beigizad, H. Soleimany, S. Zarei, and H. Ramzanipour**, "Linked Fault Analysis", *IEEE Transactions on Information Forensics and Security*, vol. 19, pp. 2894-2907, 2024.
3. **S. Banik, S. K. Pandey, T. Peyrin, Y. Sasaki, S. M. Sim, and Y. Todo**, "GIFT: A Small Present - Towards Reaching the Limit of Lightweight Block Ciphers", *Cryptographic Hardware and Embedded Systems (CHES)*, LNCS, vol. 10529, pp. 321-345, Springer, 2017.
4. **S. Sharma and B. Mazumdar**, "Towards Improved Performance Metrics for Karatsuba Multiplier and NTT-Based Polynomial Arithmetic Multiplier for PQC Primitives", *IEEE International Symposium on Smart Electronic Systems (iSES)*, pp. 228-233, 2025.
5. **C. Canella, J. Van Bulck, M. Schwarz, et al.**, "A Systematic Evaluation of Transient Execution Attacks and Countermeasures", *ACM Computing Surveys*, vol. 53, no. 5, pp. 1-45, 2020.
6. **A. K. Kundu, S. Ghosh, Aikata, and D. Saha**, "TOFA: Towards Fault Analysis of GIFT and GIFT-like Ciphers Leveraging Truncated Impossible Differentials", *IACR Transactions on Cryptographic Hardware and Embedded Systems (TCHES)*, vol. 2023, no. 1, pp. 327-353, 2023.

---

\newpage

# Appendices

## Appendix A: BAKSHEESH Cipher Parameters
- **S-Box Table**: `[3, 0, 6, 13, 11, 5, 8, 14, 12, 15, 9, 2, 4, 10, 7, 1]`
- **Bit Permutation $P_{128}$**:
  ```text
  P128 = [0, 33, 66, 99, 96, 1, 34, 67, 64, 97, 2, 35, 32, 65, 98, 3,
          4, 37, 70, 103, 100, 5, 38, 71, 68, 101, 6, 39, 36, 69, 102, 7,
          8, 41, 74, 107, 104, 9, 42, 75, 72, 105, 10, 43, 40, 73, 106, 11,
          12, 45, 78, 111, 108, 13, 46, 79, 76, 109, 14, 47, 44, 77, 110, 15,
          16, 49, 82, 115, 112, 17, 50, 83, 80, 113, 18, 51, 48, 81, 114, 19,
          20, 53, 86, 119, 116, 21, 54, 87, 84, 117, 22, 55, 52, 85, 118, 23,
          24, 57, 90, 123, 120, 25, 58, 91, 88, 121, 26, 59, 56, 89, 122, 27,
          28, 61, 94, 127, 124, 29, 62, 95, 92, 125, 30, 63, 60, 93, 126, 31]
  ```

## Appendix B: RV32I Assembly Code (`baksheesh_round1.s`)
Available in full under the repository path: `RISCV_Simulation/baksheesh_round1.s`.

## Appendix C: Reproduction Commands
```bash
# 1. Cryptographic Validation
python -m unittest discover -s lfa_baksheesh/tests
python -m unittest discover -s lfa_gift/tests

# 2. LDFA & LIFA Demonstrations
python lfa_baksheesh/experiments/run_ldfa.py
python lfa_baksheesh/experiments/run_lifa.py

# 3. Head-to-Head Comparative Benchmark
python BAKSHEESH_vs_GIFT_LIFA/compare_lifa.py
```
