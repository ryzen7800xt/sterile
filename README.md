# Sterile - Mechanical Water Filtration Simulation

A visually interactive educational simulation of mechanical water filtration systems built with Pygame. Sterile demonstrates how multi-layer filtration works to purify water through sand, activated charcoal, and fabric layers.

## Overview

Sterile is an educational tool that visualizes the water filtration process in real-time. Watch as simulated water particles (dirty and clean) flow through multiple filtration layers, getting progressively cleaned as they descend through sand, activated charcoal, and cotton sock barriers.

## Features

- **Interactive Particle Control**: Adjust the number of particles before dropping them with precision buttons (+1, +10, +50 and their counterparts)
- **Multi-Layer Filtration Visualization**: 
  - Fine Sand Layer (10 cm) - Traps smaller dirt particles
  - Activated Charcoal Layer (5 cm) - Removes odors and chemicals
  - Cotton Sock Base - Final physical sieve
- **Real-Time Simulation**: Watch water particles flow through the filter system with variable speeds based on layer density
- **Scrollable Information Panel**: Detailed explanations of each filtration layer and how they work
- **Fullscreen Mode**: Press F11 to toggle fullscreen for better viewing
- **Color-Coded Particles**: 
  - Brown particles = dirty water
  - Blue particles = clean water

## Installation

### Requirements
- Python 3.7+
- Pygame

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ReverseDrop.git
cd ReverseDrop
```

2. Install required dependencies:
```bash
pip install pygame
```

3. Navigate to the src directory:
```bash
cd src
```

4. Run the simulation:
```bash
python thing.py
```

## How to Use

### Controls

| Control | Action |
|---------|--------|
| **−50 Button** | Decrease particle count by 50 |
| **−10 Button** | Decrease particle count by 10 |
| **−1 Button** | Decrease particle count by 1 |
| **+1 Button** | Increase particle count by 1 |
| **+10 Button** | Increase particle count by 10 |
| **+50 Button** | Increase particle count by 50 |
| **Drop Water Button** | Start the simulation with selected particle count |
| **Mouse Wheel** | Scroll through the information panel |
| **F11** | Toggle fullscreen mode |

### Workflow

1. Use the adjustment buttons to set your desired number of particles (10-500)
2. Click the "Drop Water" button to start the simulation
3. Watch the particles flow through the three filtration layers
4. Observe how the particles change from dirty (brown) to clean (blue)
5. Scroll the information panel to learn more about each layer

## How It Works

### Filtration Layers

#### 1. Fine Sand Layer (10 cm)
- **Purpose**: Traps smaller dirt particles that passed through gravel
- **Cleaning Rate**: Removes 1% of dirty particles per frame
- **Water Speed**: 0.4x gravity (slowed by 60%)
- **Particle Size**: Captures particles >0.1mm

#### 2. Activated Charcoal Layer (5 cm)
- **Purpose**: Removes odors, chlorine, and chemical stains through adsorption
- **Cleaning Rate**: Removes 5% of dirty particles per frame
- **Water Speed**: 0.3x gravity (slowed by 70%)
- **Effectiveness**: Targets microscopic impurities and dissolved chemicals

#### 3. Cotton Sock Base
- **Purpose**: Final physical sieve holding the media, catches micro-sediment
- **Cleaning Rate**: 100% particle removal (all remaining dirty particles become clean)
- **Water Speed**: 0.2x gravity (slowed by 80%)
- **Function**: Acts as the last barrier before filtered water exits

### Particle Behavior

- **Dirty Particles**: Brown colored, 5px radius
- **Clean Particles**: Blue colored, 4px radius
- **Gravity Effect**: Particles accelerate 1.5x when outside filter zones
- **Reset**: Particles automatically reset at the bottom and recycle back to the top

## Project Structure

```
ReverseDrop/
├── src/
│   ├── thing.py       # Main simulation file
│   └── readme.md      # Documentation
└── README.md          # Project overview
```

## Educational Value

Sterile is designed to help students and educators understand:
- How water filtration systems work
- The importance of multi-stage filtration
- How different materials remove different types of contaminants
- The relationship between filtration speed and particle removal
- Real-world water treatment processes

## Technical Details

- **Language**: Python 3
- **Framework**: Pygame
- **Window Size**: Default 1200x800 (expandable to fullscreen)
- **Frame Rate**: 60 FPS
- **Particle System**: Dynamic, scalable from 10-500 particles
- **Performance**: Optimized for smooth visualization

## Future Enhancements

Potential features for future versions:
- Water flow rate adjustment
- Temperature effects on filtration
- Different particle types (sediment, bacteria, chemicals)
- Statistics panel showing filtration efficiency
- Export simulation data to CSV
- Custom filter layer configurations
- Before/after water quality meters

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

This project is open source and available under the MIT License.

## Author

Created by the Sterile Development Team

## Disclaimer

This simulation is for educational purposes only. It is a simplified representation of real water filtration processes. Actual water treatment systems are more complex and may require additional steps and safety measures.

## Resources

For more information about water filtration:
- [EPA Water Filtration Guide](https://www.epa.gov)
- [Water Treatment Basics](https://www.usgs.gov/water-mission/water-basics)
- [Mechanical Filtration Methods](https://www.filtration.org)

---

