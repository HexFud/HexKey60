This is my journey about how i built my keybaord

## Day 1 — *~3 hours*

Finally understood how a matrix work and connecting the first switches. Took a while to wrap my head around rows/columns and why you need diodes to avoid ghosting, but once it clicked the wiring made a lot more sense.

![Circuit Matrix](media/circuit.png)

Yes! After so many hours of work i finished the schematic but i am still not sure what microcontroller i need to use, i'll figure out later. Spent most of the time double checking pin assignments so I wouldn't have to redo the routing later.

![Circuit](media/schem.png)

## Day 2 — *~2.5 hours*

My attempt to place all the keys an other component was succesful, now it comes the wiring. Getting the footprints lined up on the 15x5 matrix took some trial and error, especially spacing them evenly for the non-standard rows.

![PCB](media/pcbk.png)

## Day 3 — *~5 hours*

PCB almost finished! It took a lot of time because the connections are A LOT. Now there are only few of them i still need to connect. This was by far the most tedious part of the whole build — routing 68 switches plus diodes and LEDs on a single board meant constantly rerouting traces to avoid overlaps.

![PCB almost finished](media/pcb1.png)

PCB Finalyy finished! Now i only need to tidy the connections and check the DRC. If it comes OK I can finally commit the diagram and PCB! Ran the design rule check a few times and fixed a handful of clearance warnings before it came back clean.

![PCB finished](media/pcbf.png)

## Day 4 — *~2 hours*

PCB officially uploaded. Now it comes the case design. Nice to close that chapter and switch to something more physical for a change.

![File uploaded](media/upload.png)

Started designign the plate, than it comes the case! Sketched out rough dimensions first to make sure the plate would actually match the PCB mounting holes.

![Plate](media/plate.png)

## Day 5 — *~3 hours*

Update:
I ran into a problem, i just realized that it isn't possible to connect the usb to the keybaord because the microcontroller is sitting right under the spacebar. A possible solution is to have a usb female-female inside the case to re-route that port to a nicer spot (probably in the front of the case)

Solution:
I searched up on the internet and i found this board https://www.adafruit.com/product/4090?hl=en-US&utm_source=chatgpt.com (Adafruit USB Type C Breakout Board) so my plan is to screw this into the case and then connect it into the PCB. Soon after i discovered that were 0 footprints about this board so i decided to create my own, with the basic pins with simple thru-hole and later I will use some jumper wires to connect it so i have more flexibility on where to put this board. Building the footprint from scratch meant carefully measuring the hole spacing off the product photos since no datasheet drawing was available.

![My footprint](media/footprint.png)

## Day 6 — *~3 hours*

Big update on the project. 
To make the USB breakout board work, I need to manually solder the micro-USB pins straight onto the board. There won't be any traces for D+ and D- on the PCB because those pins on the microcontroller are hidden right under the USB port and aren't visible in the schematic.
In the meantime, I've also worked on the case and designed the bottom part with some room for the USB cables, and added a little plate under the USB-C breakout board so I can screw it down securely. That part's done, though I had to tweak it a bit because the keys on the PCB weren't lining up right.

![Plate](media/plate1.png)

After a bit of 3D modelling i have made a shape for the bottom of the case, now i need to polish it up and then design the top. Went through a couple of iterations of the walls and standoffs before the fit felt solid.

![Bottom case](media/casebot.png)

## Day 7 — *~1.5 hours*

Update:
After a bit i came to a conclusion that I don't need to design the top part of the case because I Have designed the pcb and the plate with holes to mount them directly into the bottom part of the case. So I will now code the firmware! Flashing QMK and mapping the layout went pretty smoothly once the hardware was actually done.

## Day 7 — *~6 hours*
Revisioned one last time the project and added some serigraphy, added a GND plan and fixed more than 200+ errors! Now we only need to produce the final product

Final update on this journey, i finished up the project and now i am gonna upload all the files and write a nice README

Time spent on this project: about 26 hours
