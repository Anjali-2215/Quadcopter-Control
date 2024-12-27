"""
Entry point for the simulations.
We have 3 simulations:
- sim1 (default): Human, PID, SAC(v2_5000000), DQN
- sim2: Manual(Human), PID, SAC1(v1_3330000), SAC2(v2_5000000)
- sim3: Same drones as sim1 but bigger window and more targets

Usage:
python -m quadai        -> sim1
python -m quadai sim1   -> sim1
python -m quadai sim2   -> sim2
python -m quadai sim3   -> sim3
"""

import sys
import warnings
import quadai
from quadai.balloon import balloon

warnings.filterwarnings("ignore", category=FutureWarning)

def main():
    sim_mode = "sim1"
    if len(sys.argv) > 1:
        if sys.argv[1] in ["sim1", "sim2", "sim3"]:
            sim_mode = sys.argv[1]
    balloon(sim_mode)

if __name__ == "__main__":
    print("Quadcopter Simulation, By Utkarsh, Adarsh, Amit")
    print("Final Year Project, Electronics and Instrumentation Engineering Department, NIT Silchar")
    main()
