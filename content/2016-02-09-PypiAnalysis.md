Title: PyPi Dependency Analysis
date: 2015-07-26 05:00
comments: true
Category: Visualization
Tags: Python, web-scraping
Slug: pypi-analysis
Author: Kevin Gullikson


If you use the Python programming language, you have probably run the command

```bash
pip install [package]
```

at some point. What you may not know is the magic happening behind the scenes. The `pip` command
is connecting to the [Pypi server](https://pypi.python.org/pypi) and searching for the package you want. 
Once it finds that package, it downloads and runs a special python file titled `setup.py`, which contains a 
bunch of metadata for the package. 

Knowing this, I decided to see what I could learn from the metadata available in the `setup.py` file for 
every package on the Pypi server. There are a few things that are conceivable:

- Parse all of the dependencies from every package. By dependencies I mean other python packages that the given package relies on.
- Parse the package description, and try to do something fun with it. Maybe I will write a [Markov chain text generator](http://kgullikson88.github.io/blog/markov-chain.html) at some point to generate python package names and descriptions. Another more interesting thing would be to analyze the description with some natural language processing algorithm
- Tally up the version strings for each of the packages, and find weird ones/outliers.

I might visit the other options in a later post, but here I will be looking at the dependencies. This post 
focuses on a programming language, and will necessarily be more technical than the other ones. Pretty 
pictures near the bottom.

## Parsing Package Dependencies

Still here? Cool, let's get into how I did it. The first thing I needed to do was just figure out what the
dependencies of a given package are. That turned out to be way harder than it has any right to be. The 
command

```bash
pip show [package]
```

gives a bunch of metadata for the given package, including everything it requires to run, but **it only 
works if you have the package installed!** I am not about to install every package on pypi on my or anyone 
else's computer, so had to look for a more hacky way to do this. It turns out [Olivier Girardot](
https://ogirardot.wordpress.com/2013/01/05/state-of-the-pythonpypi-dependency-graph/) did a similar project 
a few years back, so I took their code as a starting point. 

The first thing I did was download every package on pypi, and extract the `setup.py` file and any file or directory with the work 'requirement' in it.

```python
#TODO: Enter code to do this here.
```

The first step left me with a bunch of directories that contain all the metadata for every pypi package (TODO: package and add this to Downloads...). Next, I used a slightly modified version of the [requirements-detector](https://github.com/landscapeio/requirements-detector) package to parse out the requirements. The package does the following:

1. Search the `setup.py` file for an `install_requires` keyword, and attempt to parse package names out of that.
2. If step one fails, search any file with the word 'requirement' in it, and look for things that look like python requirements
3. Failing **that**, search any file that ends with '.txt' in any directory that contains the word 'requirement' for stuff that looks like python requirements.
4. Output the requirements found to a text file

Of the [Ntotal] packages on pypi, I was able to parse requirements for [Nreq]. The remaining packages probably do require other packages, but the `setup.py` file is written in such a way that it was difficult to parse. Sadly, my [TelFit package](https://pypi.python.org/pypi/TelFit/1.3.2) is one of those failures because it defines the install_requires keyword programmatically. Leaving those out probably biases the result in some complex way, but I am sick of munging so let's move on to the fun part.

## Dependency Analysis

Now that I have all of the dependencies for (most of) the packages on the pypi server, I want to see what I can learn. The first thing is to make a network graph of dependencies:

TODO: Make picture of the graph that links to the javascript version...

TODO: Describe the graph

TODO: Figure out other interesting statistics.

- Histogram of the number of dependencies for each package.
- [Centrality measures](https://en.wikipedia.org/wiki/Network_theory#Centrality_measures)
- Compute the [PageRank](https://en.wikipedia.org/wiki/PageRank) of each node, make a histogram similar to the first stat.
