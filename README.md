# FlowCalcs

## Model

Simulates the movement of water through the DH irrigation system using currently avaiable specs (reservoir sizes and cycle times) 

At minute intervals the water level in each reservoir is calculated based on the outflow and inflow rates (as determined by the Cycle Out and Cycle In times
shared by the DH team). At the completion of a cycle a cycle loss rate is applied to the remaining amount of water, and then the reservoir begins refilling 
with a depleted amount of water. 

Total consumption is calculated by comparing initial reservoir level and adjusted reservoir levels after cycle loss rate is applied.

