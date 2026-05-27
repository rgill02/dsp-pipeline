# dsp-pipeline
A framework for creating data processing pipelines geared towards digital signal processing applications.

## Motivation

I am working on a processing pipeline for side scan sonar. I have one processing chain for some early development data where we record raw data. Then we push some more processing functions from the post processor down into the sonar. Now I have a slightly different chain with a different reader and less processing stages. In the future we will push more down into the sonar, changing the chain again. On top of that, the different data formats come with variations themselves: some collections have gps data, some have IMU data, some have both, some have none. This means a whole bunch of readers, and then some variations in the processing chain depending on whether this auxillary data is present or not. Then there are some blocks, like a beamformer, where I will want to try out various algorithms and for each algorithm tweak various parameters. And then I may want this chain to save its output to a file or stream it to a display, or both. I have found myself copying and pasting processing chain code and the modifying it over and over again. So I need a flexible chain where I can design processing stages that fit a certain pattern and then at a high level select the reader I want, the various stages and how they tie together, give the input parameters to the various stages, and then I have a chain I can run. I want this chain to process one sonar ping at a time so that it works for both post processing and real time streaming. And I want this chain to take advantage of multi-core machines to process the data fast since streaming one ping at a time isn't as efficient as batch processing. In the end I would love a high level config file that describes a processing chain where I or someone else who is not familiar with the code can load the config and press go and I get processed data. And people who do have DSP knowledge can write new blocks for the chain.

## Description / High Level Overview

This library will implement and easily reuseable, customizeable, and extendable data processing pipeline. It will allow users to develop processing blocks according to specific patterns and then stitch those blocks together easily in a pipeline with tuneable parameters. The pipeline will be able to handle various sources and sinks. It will stream the data, one data chunk at a time, but will queue up the data in queues between stages so that each stage can run in its own thread to take advantage of multi-core machines. Once a user has defined various processing blocks, he should be able to easily create a bunch of variants of processing pipelines all by modifying a high level config file/structure.

## Past this point is from the [template](https://gist.github.com/DomPizzie/7a5ff55ffa9081f2de27c315f5018afc) I found and still needs to be updated

## Getting Started

### Dependencies

* Describe any prerequisites, libraries, OS version, etc., needed before installing program.
* ex. Windows 10

### Installing

* How/where to download your program
* Any modifications needed to be made to files/folders

### Executing program

* How to run the program
* Step-by-step bullets
```
code blocks for commands
```

## Help

Any advise for common problems or issues.
```
command to run if program contains helper info
```

## Authors

Contributors names and contact info

ex. Dominique Pizzie  
ex. [@DomPizzie](https://twitter.com/dompizzie)

## Version History

* 0.2
    * Various bug fixes and optimizations
    * See [commit change]() or See [release history]()
* 0.1
    * Initial Release

## License

This project is licensed under the [NAME HERE] License - see the LICENSE.md file for details

## Acknowledgments

Inspiration, code snippets, etc.
* [awesome-readme](https://github.com/matiassingers/awesome-readme)
* [PurpleBooth](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2)
* [dbader](https://github.com/dbader/readme-template)
* [zenorocha](https://gist.github.com/zenorocha/4526327)
* [fvcproductions](https://gist.github.com/fvcproductions/1bfc2d4aecb01a834b46)
