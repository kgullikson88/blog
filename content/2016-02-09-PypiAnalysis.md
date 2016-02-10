Title: PyPi Dependency Analysis
date: 2016-02-12 05:00
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
a few years back, so I took his code as a starting point. 

The first thing I did was download every package on pypi, and extract the `setup.py` file and any file or directory with the word 'requirement' in it.

```python
def extract_package(name, client=xmlrpclib.ServerProxy('http://pypi.python.org/pypi')):
    for release in client.package_releases(name):
        outdir = 'packages/{}-{}/'.format(name, release)
        doc = client.release_urls(name, release)
        if doc:
            url = None
            for d in doc:
                if d['python_version'] == 'source' and d['url'].endswith('gz'):
                    url = d['url']
            if url:
                req = requests.get(url)
                if req.status_code != 200:
                    print("Could not download file {}".format(req.status_code))
                else:
                    #print(outdir)
                    ensure_dir('{}'.format(outdir))
                    with open('/tmp/temp_tar', 'w') as tar_file:
                        tar_file.write(req.content)
                    with open('/tmp/temp_tar', 'r') as tar_file:
                        return _extract_files(tar_file, name=outdir)

for package in packages:
    extract_package(package, client)
```

The first step left me with a bunch of directories that contain all the metadata for every pypi package (TODO: package and add this to Downloads...). Next, I used a slightly modified version of the [requirements-detector](https://github.com/landscapeio/requirements-detector) package to parse out the requirements. The package does the following:

1. Search the `setup.py` file for an `install_requires` keyword, and attempt to parse package names out of that.
2. If step one fails, search any file with the word 'requirement' in it, and look for things that look like python requirements
3. Failing *that*, search any file that ends with '.txt' in any directory that contains the word 'requirement' for stuff that looks like python requirements.
4. Output the requirements found to a text file

Of the $\sim 74000$ packages on pypi, I was able to parse requirements for 20522. The remaining packages probably do require other packages, but the `setup.py` file is written in such a way that it was difficult to parse. Sadly, my [TelFit package](https://pypi.python.org/pypi/TelFit/1.3.2) is one of those failures because it defines the install_requires keyword programmatically. Leaving those out probably biases the result in some complex way, but I am sick of munging so let's move on to the fun part.

## Dependency Analysis

Now that I have all of the dependencies for (many of) the packages on the pypi server, I want to see what I can learn. The first thing is to make a network graph of dependencies (click on the image for an interactive version):

<a href="http://kgullikson88.github.io/blog/Javascript/PypiGraph/Requirements_clipped/network/index.html">
  <img src="Images/PypiGraph.png" >
</a>

Comparing this network graph to the version that Olivier Girardot made a few years ago, we immediately see
that the python ecosystem has grown tremendously and become much more connected. The bulk of the network is
centered on the `requests` module, indicating the python is largely a web language (much to the chagrin of me the scientist!) A good sign is the size of the testing and documentation cluster, which is just above the requests cluster. The pydata stack, which includes `numpy`, `scipy`, `matplotlib`, and `pandas`, is in the upper left. I'm not
sure what is going on with the clump that is separated from the rest near the bottom; I think it might be iphone/android app frameworks.

The graph is pretty and very fun to play with, but what can we actually learn from it?

TODO: Figure out other interesting statistics.

- Histogram of the number of dependencies for each package.
- [Centrality measures](https://en.wikipedia.org/wiki/Network_theory#Centrality_measures)
- Compute the [PageRank](https://en.wikipedia.org/wiki/PageRank) of each node, make a histogram similar to the first stat.
