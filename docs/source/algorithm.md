# Modeling Random Telegraph Signal



## What is Random Telegraph Signal?

Random Telegraph Signal is the result of a randomly occurring jumps between discrete voltage levels, whose source is the Metal-Oxide Semiconductor Field Effect Transistor (MOSFET) in each pixel in a CMOS sensor.
RTS shows up in bias frames, and any other time where the incoming signal is very low. This is because the temporal signal or light signal is usually dominant over RTS, which can have a read noise anywhere about 20e- and above.
Due to correlated double sampling, where the read out value of a pixel is taken as the difference between the activated pixel voltage and the reset voltage, we see a multi-modal distribution of data points.



## Gaussian Mixture Models

## Error Propagation