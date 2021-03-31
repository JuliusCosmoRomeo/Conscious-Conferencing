# Conscious Conferencing

## Applying Attention Feedback in Video Conferencing to Increase Group Connectivity

The goal of this project was to build a demonstration tool showing how collective attention feedback can enhance group connectivity in online meetings. 

### What this tool does

![image](https://user-images.githubusercontent.com/10089188/113192279-dac72f00-925e-11eb-91f8-3446e766237f.png)

![image](https://user-images.githubusercontent.com/10089188/113192290-ddc21f80-925e-11eb-998e-d8cdaf01c52a.png)

![image](https://user-images.githubusercontent.com/10089188/113192302-e0247980-925e-11eb-823f-cc9861cec3d5.png)

This tool reflects group attentiveness in online meetings to all team members by analyzing gaze direction to infer attention. 
In the current prototype the further a user looks away from the screen the lower their attention score and the lower the attention of a user the more their video tile will blur. 
Additionally, if the aggregated distraction in the group is relatively high (e.g. one user is very distracted or multiple users aren’t attentive), not just their individual tiles will blur but also the screens of all other participants. 
The hypothesis behind this approach is that this form of collective attention feedback would increase collective consciousness and encourage participants to stay attentive as this would impact the whole group’s communication.

### Future work

![image](https://user-images.githubusercontent.com/10089188/113192793-840e2500-925f-11eb-8a4c-f5feb5958c62.png)



Other signals that might correlate with group connectivity and could be analyzed and reflected by the tool are   
- interoceptive biosignals like the heart rate [using remote photoplethysmography](https://www.researchgate.net/profile/Daniel-Mcduff/publication/308747669/figure/fig1/AS:614288729309227@1523469254940/Schematic-of-remote-photoplethysmographic-PPG-imaging-using-a-digital-cameras-1.png) which could be used to analyze biosynchrony across participants
- analyzing emotional states using camera vision and ML (e.g. using [OpenFace](https://github.com/cmusatyalab/openface))
- biomimicry as indicator for the Chameleon effect (people who mimic each other are more liked): [calculate the euclidean distance](https://github.com/cmusatyalab/openface/blob/master/demos/compare.py) between two faces as a proxy for mimicry
