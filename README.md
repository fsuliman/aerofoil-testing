# aerofoil-testing
Tooling required to test various hypotheses regarding what causes lift forces on aerofoil structures.


'Tooling' here primarily refers to the following goals of this repository:
1. The circuit assembly and configuration of a strain guage taking the form of a wheatstone bridge capable of measurement of mass in the range 0 to 1kg
2. Development of the software in python that supports the calibration and query of the strain gauge to report on values of uplift force being experienced by various aerofoil structures under conditions of:
  a) varying airspeed at constant angle of attack and constant camber
  b) varying angles of attack at constant airspeed and constant camber
  c) varying cambers at constant angle of attack and constant airspeed

In addition the project includes the development of a GUI based application for exposing the measurement capture and data graphing functions via a graphical user interface for ease of use by an elementary school student in the USA.  Application functions may variously cover:
  1. workflow to calibrate the strain gauge
  2. management of CSV formatted data files to which an experiment's dependent uplift force variable and independent variable values (air speed, angle of attack,camber) can be conveniently recorded
  3. rendering of experiment results in graphical form to a suitable chart type, either static x-y plot, near real time-time series plot, or box plot etc., depending on time available for development
