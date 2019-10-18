# Corrie

## Features

Corrie is a software program for providing building design advice based on building performance simulation.
It is intended for very early in the design process before even the building shape has been decided. The 
software may be used for [ASHRAE Standard 209](https://www.techstreet.com/ashrae/standards/ashrae-209-2018?product_id=2010483) 
Modeling Cycle #1 “Simple Box Modeling.” The software may be useful as part of a bid or before a 
charrette. It requires only a few inputs and uses EnergyPlus and OpenStudio to produce a series of 
simulations that explore how the building design is impacted by a variety of energy efficiency measures 
such as:
 
 - floorplate aspect ratio
 - number of stories
 - orientation
 - wall insulation 
 - roof insulation
 - amount of windows
 - lighting power 
 
Corrie creates a PowerPoint presentation based on the simulation results for the measures selected and options chosen.
Each type of measure is shown as a graph on a slide with energy usage for each of the options selected.
In addition, a slide with the end-use breakdown is included as well as a slide on the assumptions used.


## Installing Corrie

To install Corrie on Windows:

- First, install [OpenStudio 2.8.0](https://github.com/NREL/OpenStudio/releases/tag/v2.8.0)
Other versions of OpenStudio have not yet been tested with Corrie and may not work.

- Download the latest Corrie.zip file from [releases](https://github.com/JasonGlazer/Corrie/releases). You may need to click on "assets" to see the zip file.

- Unzip the Corrie.zip file to a directory like c:\Corrie

While Corrie should also work on Linux and MacOS, they have not been tested yet. 
If you want to try it on Linux or MacOS clone the repository and let me know if it works.

## Tutorial

To run Corrie, double click on the Corrie.exe file in the directory that you installed corrie. It may be in:

    C:\corrie\corrie.exe

This should open up the user interface:

![Initial screen](/images/InitialScreen.PNG)

Select the building, the direction the front of the building faces, and the baseline code where the building is located using the dropdown options.

![Building, Front Faces, Baseline Code](/images/building-faces-code.png)


Select a weather file by clicking on the "..." button . If you don't have a weather file, you can download an EnergyPlus epw file from [climate.onebuilding.org](http://climate.onebuilding.org/)

![Select weather file](/images/select-weather-file.PNG)

Enter the main occupancy areas for the building. For many buildings, only one occupancy area is shown, but 
some buildings have multiple occupancy areas. If you don't need one, leave it as a zero.

![occupancy areas](/images/occupancy-areas.PNG)

For each slide, you click on the option being simulated will show up next to it.

![slides and options](/images/slides-and-options.PNG)

Each checked option under each slide that is checked represents an individual simulation so you may want 
just to have a few checked to begin with to see if everything is working for you. After that you can 
check as many as you want but will take some time to simulate many options with EnergyPlus. You can also 
change the order that the slides appear by using the Up and Down buttons.

Next, save your file using the File menu. This should automatically create the name of the PowerPoint file
that is created. The PowerPoint file must be closed and is overwritten each time the simulations are run.

Next, click "Run Simulations" and work on something else for a while. 

When the simulations are complete, find where you saved your file and open the PowerPoint file to see the 
results. The slide deck should start with a slide showing the selections you made and look something like:

![presentation assumptions](/images/presentation-assumptions.PNG)

The next slides should correspond to each one you selected.

![presentation roof insulation](/images/presentation-roof-insulation.PNG)

For now, only the total net site energy is being reported.

An end-use breakdown is also included as is a summary of the selected option for each slide (the one with the lowest net site energy).

You may want to copy and paste the slides you want into another presentation file because they will be overwritten
when you click "Run Simulation" the next time.

## Support

Ask questions on [BLDG-SIM](http://onebuilding.org/) or on [Unmethours](https://unmethours.com/questions/).

You can post issues under the issues tab above if you find any bugs. 

## Status

This is just an Alpha version. I have a lot of additional features in mind. I welcome your feedback.


