# TODO / notes 

## TODO
- [ ] Work out how I want to be storing the parsed data in code, and when written to file.
- [ ] Think of a better name for the GpsFixData class, you can't completely change what it does and keep the same name.
- [ ] Impl args for the `run` method on the GpsFixData class things like.
    - choose whether the data is automatically written to file or not.
    - choose a set length of time (or number of lines) for the parser to run for, before terminating itself. 
- [ ] Add some form of auto com-port check? 
- [ ] Look into, and possibly implement a fetch to google maps api to get location data once a fix has been established.
- [ ] Use satellite data to produce a map of satellite locations relative to the receiver module? (Extend to 3D?)

## Notes / Thoughts 
[Storing-nmea-data]
Currently I'm unsure if using dictionaries to store the NMEA data is the best way too do it, I guessed it would make writing to a json easier, but I'm unsure if there isn't a better way of going about this for the sake of readability in the code? I feel like making a bunch og get calls when I need to access values feels messy; I've considered wrapping the data in it's own class, if this was rust i would just use structs as a custom data type...

