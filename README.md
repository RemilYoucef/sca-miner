# SCA-Miner
Subgroup Discovery with Hierarchical Target Concepts: Application to Java Heap Memory dumps

## Overview
<img  alt="" src="./overview.png" style="width: 100%;" />

## Data:
The data file contains the input files required to run our solution dubbed SCA-Miner, this folder contains 3 sub-folders:

**original data**: In this repository we find 3 csv files:
1. Jmaps: this file contains the memory snapshots generated manually from normal behaving servers (i.e. healthy servers) each sunday morining during a 3 month period.
2. Jmaps-OOM: this file contains the memory snapshots triggered automatically after a memory crash.
3. all-instances-metadata: this file contains the descriptive attributes (env features) for the servers concerned by our study.

We gave two examples for sales (vt) and factory (sv) servers to show how to generate the corresponding hierarchical structures fed to the model, the impelementation details are located in **data-preprocessing** folder (two notebook examples are provided) 

**data-sv**: this repository contains data corresponding the factory servers and we have:
- itemNames.txt: contains the id and the corresponding name of each concept (class and/or package) (e.g., [id = **78**, concept = **java.util.Vector**])
- DAG.txt: it gives the hierarchy structure, i.e., each line of this files depicts a parent child relation based on ids of items and it is common for all memory (e.g., **195** = java.util, **78** = java.util.Vector)
- supportAllSnapshots.txt: contains the observed value of each item (the xHat values) of each memory snapshot. (e.g., idSnapshot = **0**, concept = **java.util.Vector**, size = **3** MB)
- supportAllZeros.txt: contains the values used to infer the expected values of each concept (i.e., they give xBar after normalization by the total size of all the snapshot heap sizes).
- snapshotNames.txt: contains the id and the corresponding index (server,timestamp) of each memory snapshot.  
- probasModel.json: this file contains the values of factor functions (conditional probabilities), this file is produced based on the algorithm **code-factor**.
- minerSD: this file is an pickle object (dictionary) that stores all the conditional and marginal probabilities of concepts as well as its observed and expected values of each memory snapshot, this file is produced based on the algorithm **code-factor**.

## Algorithms:

In the folder **code-factor**, we highlight the whole procedure to derive and calculate the conditional and mariginal probabilities for the hierarchies, the provided notebooks show the necessary steps to build those hierarchies. 
In the folder **subgroup-miner**, we perform the mining algorithm i.e., SCA-Miner approach to output the most interesting patterns. Examples are given in the notebook **subgroup-miner-sv** for factory servers. 
