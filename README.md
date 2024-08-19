# APS360-57
Group 57's repository for the APS360 course at the University of Toronto.

## Project Abstract
We apply a Physics-Informed Neural Network (PINN)-based method to extend and increase the time resolution of fluid flow simulations. Given timesteps and data coordinates, the PINN can extrapolate and interpolate timesteps of velocities and pressures in periodic fluid flow fields. The PINN achieves predictions highly consistent with the physical model characterized by Navier-Stokes PDEs, with errors of predicted velocity and pressure values are between 10-15% and 10-25% of the training data magnitudes respectively.

## File Structure
Data: Training data, scripts for generating and processing ANSYS data\
Source: Scripts for models, training, testing\
Figures: GIF animations of predicitons\
Plotting: Code for generating GIF animations from Data or Predictions files\
Predictions: Output folder for flow field predictions by models\
Trained models: Saved .pt models
