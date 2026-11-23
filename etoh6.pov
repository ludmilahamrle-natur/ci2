#version 3.7;

#include "etoh.pov"

global_settings {
  assumed_gamma 1.0
  ambient_light rgb <0.45, 0.45, 0.45>
}

background { color rgb <0.97, 0.98, 1.0> }

light_source {
  <0, 0, 14>
  color rgb <1, 1, 1>
}

camera {
  orthographic
  location <0, 0, 20>
  look_at <0, 0, 0>
  right <18, 0, 0>
  up <0, 18, 0>
}

#declare RingRadius = 6.0;
#declare MoleculeIndex = 0;

#while (MoleculeIndex < 6)
  #declare Angle = MoleculeIndex * 60;
  object {
    mol_0
    translate mol_0_center
    rotate <0, 0, Angle>
    translate <RingRadius * cos(Angle), RingRadius * sin(Angle), 0>
  }
  #declare MoleculeIndex = MoleculeIndex + 1;
#end
