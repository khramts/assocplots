# Assocplots: a python package for static and interactive visualization of multiple-group GWAS results

## Table of Contents:
**[Background](#background)**  
**[Implementation](#implementation)**  
**[Installation](#installation)**  
**[Documentation](#documentation)**  
**[Examples](#examples-and-tutorials)**  
**[Alternative Resources](#alterative-resources)**  


##Background:
Over the last decade plethora of genome-wide association studies (GWAS) data has been generated, requiring development of novel tools for visualization of large quantities of data. Quantile-quantile plots and Manhattan plots are the classical tools which have been utilized to present GWAS results and identify variants that are significantly associated with traits of interests. However, static visualizations are rather limiting in the information that can be shown. It is only in recent years that dynamic, interactive visualization has become more widely adopted, however it has not yet become a routine part of GWAS data analysis. Interactive data visualization not only allows to more clearly represent multidimensional data, but also encourages viewer’s engagement from simple data browsing to providing a platform for answering specific scientific questions, in ways that static data cannot. Here we present a package for viewing GWAS results not only using classic static Manhattan and quantile-quantile plots, but also through interactive extension which allows to visualize data interactively: zoom into dense regions, quickly obtain underlying details (e.g. SNP rs number or gene name, base pair position, p-value) by selecting a peak of interest, and visualizing the relationships between GWAS results from multiple groups. Furthermore, a scientist might be interested in comparing GWAS results from multiple groups: (1) various traits/phenotypes measured in a group of individuals, (2) same phenotype measured among distinct groups of individuals such as males and females, (3) expression quantitative loci measures across different tissues, and (4) various experimental conditions such as before and after drug treatment, to name a few. Our tool makes it possible to browse multiple charts in real-time to better understand the relationships among multiple groups.

## Implementation: 
Assocplots is implemented as a package for the Python programming language. Its basic functionality includes plotting interactive data visualization for viewing in the browser as well as static publication quality plots. The package is designed to be used both in Jupyter notebooks and in command line. Visualizing GWAS data in a web-based document (notebook), ensures data analysis reproducibility and makes it conveniently sharable with collaborators via online repository like GitHub. The assocplots package is open source and distributed via GitHub along with examples, documentation and installation instructions.

## Installation:
In order to install assocplots run the following command in console:
```
pip install https://github.com/khramts/assocplots/archive/master.zip
```

## Brief Documentation:

### Static plots features:

#### Classic Manhattan plot
1. X-axis: chromosome and base pair (both numeric and alphabetical names) 
2. Y-axis:  -log10(p-value) or other values such as the effect size can be specified
3. Inverted Manhattan plot for two groups for easier visualization of peak differences  

#### Classic quantile-quantile plot
1. Multiple groups plotting
2. Genomic Inflation Factor, λgc, calculation
3. Confidence Intervals (CI) estimation

#### Figure generation  
Figures can be saved in raster format (i.e. png and jpg) and vector format (i.e. pdf and ps).

### Interactive module features

#### Dynamic Manhattan and QQ plot 
1. Info pop-up: Hovering over a point reveals information about the plotted SNP
2. Group comparison: Selecting a set of SNPs in one graph automatically highlights those same SNPs in the other graph. A table is generated below the graphs, listing all the selected SNPs and information about those SNPs including the position, and the test statistic across groups. 
3. Zoom-in and -out

#### Visualization Sharing
Interactive plots can be saved as notebooks and self-contained html files that can be shared with colleagues via usual sharing platforms (GitHub, Dropbox, Google Drive, etc.) and opened in any modern web browsers on any operation system.


After installing assocplots, everytime after launching python, you will need to import the function which you would like to use.  

###### Quantile-quantile (QQ) plot import
```
from assocplots.qqplot import *
```
###### Manhattan plot import 
```
from assocplots.manhattan import *
```
###### Interactive QQ and Manhattan plot
```
from assocplots.interactive import *
```

## Examples and tutorials
An explaination of how to use this package is presented in these two examples.

[Example 1](https://github.com/khramts/assocplots/blob/master/Tutorial.ipynb) Static Manhattan and QQ plot   
[Example 2](https://github.com/khramts/assocplots/blob/master/Tutorial_interactive_plots.ipynb) for Interactive Manhattan and QQ plot and its inbrowser [visualization](http://khramts.github.io/output.html)

## Alterative resources
Link to a list of alternative [resources](https://github.com/khramts/assocplots/blob/master/Alternative_tools.md).

