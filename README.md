# CISC 499 Undergraduate Project: 
# Automated Wifi Router Location Adjustment

## Introduction

A very common challenge often faced in public places or office environments is the placement of the wifi access routers.   

As routers might be operating on the same frequency, having multiple routers in proximity of each other could lead to high interference which in turn leads to a degradation in network performance. Furthermore, the location of the router impacts coverage.   

If a router is placed in an area with no one to serve, it is considered a waste of resources. Additionally, as people in public places, such as shopping malls, are constantly moving around, fixing the location of the routers might not be optimal. 

Hence, one way to solve all those issues is to allow some sort of mobility for some of the routers such that they are able to automatically adjust their locations depending on the loading as well as interference conditions. 

For instance, if a router senses that in its current location there is few people to serve, it might consider moving around to serve more people. 

Similarly, if a router is experiencing high interference, it can adjust its position as to achieve better performance. 

In this project, the students are expected to consider a scenario with multiple fixed router locations and one mobile router. The mobile router can be considered as a reinforcement learning agent that senses the environment and adjusts its position accordingly.


## Background of the Project

The placement of wifi routers is a difficult problem faced when it comes to
public and office environments. Network administrators face this problem
constantly. It is both expensive and tedious to plan out and implement networks
with fixed location routers. Having multiple fixed routers in an environment can
introduce interference as well as have the chance for some of them to be
underutilized and ultimately considered to be a wasted resource and produce an
overall greater implementation cost for the network. In these times during the
pandemic, both office and public environments are seeing sparse and sporadic
traffic from day to day with the introduction of reductions in capacity of buildings.
In post-COVID-19 times, we believe that our project can have a great impact on
creating a dynamic network that can change its physical layout to adapt to the
physical changes around it.

Wireless frequency use is regulated in many countries and many routers
produced today operate at similar frequencies, two of the most widely used being
2.4GHz and 5GHz [1]. Routers that are fixed in locations and operate at similar
frequencies can interfere with one another causing degradation in network
performance for a device operating on the network. These areas of overlap
between the routers’ coverage induce some background noise into the intended
signal if the device is located within these areas. This interference can be
measured using the Signal-to-noise ratio (SNR) which is a measurement that
compares the strength of the desired signal in relation to that of the strength of
background noise. The strength of a signal, whether that be the intended signal or
of the noise can be calculated using the inverse square law based on the distance
from the router. The second problem with fixed router networks is that routers
may tend to be underutilized as they could be located in a place where there is
very infrequent traffic due to lack of people in that area or the movement of
people throughout a day changes. A router in these areas of sporadic or low
traffic areas can be considered a waste of resource as the router is being
underused with respect to its full potential.


The overlying problem at hand is a way to manage the interference
between routers while also making sure that all routers are utilized. One way to
resolve these issues is to produce a router that has mobility and is able to relocate
itself throughout an environment. The approach our group took to advance a
solution to this problem is an implementation of a router with an A.I. agent and
mobility capabilities. By enabling a router to move around an environment it is able
to relocate itself throughout an environment to optimize the network that it is a
part of. By developing a reinforcement learning algorithm for the router, it is able
to explore its environment and can determine where the optimal location it should
relocate itself to in order to optimize both surface-area coverage as well as the
number of devices serviced. For example, If the A.I. agent router feels that it has
too much interference with one of the fixed routers in the area. It may determine
that the best option is to relocate itself to minimize the SNR between itself and the
fixed router. This helps to minimize interference with other routers and in turn
improve the overall performance of the network. Also if the A.I. agent router is
being underutilized, it may decide to change positions to a place where there are
more people to serve. The goal of our project is to implement an effective
reinforcement learning algorithm that can be applied to a wireless router with
mobile capabilities, and when placed in a new environment with other fixed
routers, can adapt and learn to optimize the network it is placed in.
