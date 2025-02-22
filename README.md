# aerofoil-testing
Tooling required to test various hypotheses regarding what causes lift forces on aerofoil structures.


'Tooling' here primarily refers to the following goals of this repository:
1. The circuit assembly and configuration of a strain guage taking the form of a wheatstone bridge capable of mass measurement in the range 0 to 1kg
2. Development of the software in python that supports the calibration and query of the strain gauge to report on values of uplife force being experienced by various aerofoil structures under conditions of:
  a) varying wind speed at constant angle of attack and constant camber
  b) varying angles of attack at constant wind speed and constant camber
  c) varying cambers at constant angle of attack and constant aire speed

In addition the project may involve, time permitting, the development of a GUI based application for placing the various tooling functions behind a graphical user interface for ease of use by an elementarty school student in the USA.  Application functions may variously cover:
  1. workflow to calibrate the strain gauge
  2. management of CSV formatted data files to which an experiment's dependent uplift force variable and independent variable values (air speed, angle of attack,camber) can be conveniently performed
  3. rendering of experiment resolts in graphical form to a suitable chart type, either static x-y plot or near real time-time series plot or both depending on time available for development