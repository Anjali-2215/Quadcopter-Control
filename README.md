# Quadcopter-Control  

## Main Game  
The main environment involves controlling a drone to hit as many balloons as possible within a time limit, competing against AI drones.  

### Implemented Algorithms  

- **Human**: Control the propellers using the arrow keys.  
- **PID**: A Proportional-Integral-Derivative controller that uses the error between the drone's position and the target position to output appropriate propeller thrusts.  
- **SAC**: A Soft Actor-Critic (Reinforcement Learning) agent that trains itself over multiple episodes of the game, experimenting with different actions and learning from the rewards it receives.  

---

## Usage  
The games are available to play as a Python package.  

### Prerequisites  
Ensure that Python is installed on your system.  

---

## Installation and Running the Game  

### Step 1: Downgrade pip (if needed)  
```bash
python -m pip install pip==21
```  

### Step 2: Install the package using pip  
```bash
pip install git+https://github.com/Anjali-2215/SACopters.git
```  

### Step 3: Run the game  
To play the balloon game:  
```bash
python -m quadai
```  

- Control your drone using the arrow keys.  
- Hit as many balloons as possible within the time limit.  

---

## Alternative Setup  
You can set up a similar environment using Anaconda Navigator.  

---

## License  
This project is licensed under the MIT License. Refer to the LICENSE file for more details.  

---

## Contributing  
If you wish to contribute to this project, please fork the repository and use a feature branch. Pull requests are warmly welcomed.  

---

## Contact  
If you have any questions or suggestions, feel free to open an issue or contact me directly at **meetanjali12911@gmail.com**.  

--- 
