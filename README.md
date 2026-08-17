# dsp-pipeline
A framework for creating data processing pipelines geared towards digital signal processing applications.

## Description / High Level Overview

This library will implement and easily reuseable, customizeable, and extendable data processing pipeline. It will allow users to develop processing blocks according to specific patterns and then stitch those blocks together easily in a pipeline with tuneable parameters. The pipeline will be able to handle various sources and sinks. It will stream the data, one data chunk at a time, but will queue up the data in queues between stages so that each stage can run in its own thread to take advantage of multi-core machines. Once a user has defined various processing blocks, he should be able to easily create a bunch of variants of processing pipelines all by modifying a high level config file/structure. However, we will start with just processing stages (no sources, or sinks). These will stay simple, a lot of the features mentioned above will come later.

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
