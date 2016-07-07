# Assocplots: a python package for static and interactive visualization of multiple-group GWAS results

## Table of Contents:
**[Background](#background)**  
**[Implementation](#implementation)**  
**[Installation](#installation)**  
**[Documentation](#documentation)**  
**[Examples](#examples-and-tutorials)**  
**[Alternative Resources](#alterative-resources)**  


##Background:
Advances in genotyping, sequencing, and phenotyping techniques have resulted in large quantities of genome-wide association studies (GWAS) data. The results of GWAS are commonly summarized and displayed on a Manhattan plot and a quantile-quantile (QQ) plot and help identify single nucleotide polymorphisms (SNPs) that are significantly associated with a given phenotype. However, static visualizations are rather limiting in the information that can be shown. It is only in recent years that dynamic, interactive visualization has become more widely adopted, however it has not yet become a routine part of GWAS data analysis. Interactive data visualization not only allows clearer representation of multidimensional data, but also encourages a viewer’s engagement from simple data browsing to providing a platform for answering specific scientific questions, in ways that static data cannot. Here we present a python package for viewing GWAS results not only using classic static Manhattan and QQ plots, but also through an interactive extension which allows a user to visualize data interactively, for example: zoom into SNP dense regions, quickly obtain underlying details (e.g. SNP rs number or gene name, base pair position, p-value) by selecting a peak of interest, and visualizing the relationships between GWAS results from multiple cohorts or studies. For example our tool allows exploration of GWAS results from: (1) multiple phenotypes in a single group of individuals, (2) a phenotype measured among distinct cohorts, (3) expression quantitative trait loci measured across different tissues or cohorts, and (4) various experimental conditions such as before and after drug treatment.  Thus, our tool makes it possible to browse multiple charts in real-time to better understand the relationships among groups.

## Implementation: 
Assocplots is implemented as a package for the Python programming language. Its basic functionality includes plotting interactive data visualization for viewing in the browser as well as static publication quality plots using matplotlib. Interactive visualization is implemented via a Python interactive visualization library, [bokeh](http://bokeh.pydata.org/), that targets modern web browsers; and data wrangling is implemented with Numpy and Pandas scientific computing python libraries. All of these tools are open source. The use of python for this package makes it easily accessible to bioinformaticians, as it is one of the commonly used programming languages in the field. The package is designed to be used both in [Jupyter notebooks](http://jupyter.org/) and in command line. Visualizing GWAS data in a web-based document (notebook), ensures data analysis reproducibility and makes it conveniently sharable with collaborators via online repositories such as GitHub. The Assocplots package is open source and distributed via GitHub under the MIT license. 

## Installation:
In order to install assocplots run the following command in console:
```
pip install https://github.com/khramts/assocplots/archive/master.zip
```


## Documentation:

### Static plots features:

#### Classic Manhattan plot
1. X-axis: chromosome and base pair (both numeric and alphabetical names, so various chromosome labeling (e.g. 1, 2, chr1, X) is acceptable) 
2. Y-axis: Although -log10(p-value) is the most commonly used value for the y-axis, other values such as the effect size can be specified
3. Inverted Manhattan plot for two groups for easier visualization of peak differences  

#### Classic quantile-quantile plot
1. Multiple groups plotting: Multiple groups can be visualized on the same QQ plot for easier comparison. 
2. Genomic Inflation Factor, λgc, calculation: In GWAS population sub-structure and cryptic relatedness among subjects can lead to spurious errors, and genomic control method is commonly used correct the under-lying population stratification (Devlin et al. 1999). The static module can be used to calculate λgc.
3. Confidence Intervals (CI) estimation: The package allows to plot CIs for either the null distribution or the experimental data. When multiple groups are plotted, CI can be displayed for each group.  

#### Figure generation  
Assocplots supports matplotlib plotting backends and thus can save figures in raster format (i.e. png and jpg) and vector format (i.e. pdf and ps).

### Interactive module features

#### Dynamic Manhattan and QQ plot 
1. Info pop-up: Hovering over a point reveals information about the SNP/gene, such as the name (SNP rs number), chromosome, base pair location, and the statistic reported on the y-axis (-log10(p-value) or effect size). 
2. Group comparison: Selecting a set of SNPs in one graph automatically highlights those same SNPs in the other graph (a different phenotype, population, condition, etc.) Additionally, a table is generated below the graphs, listing all the selected SNPs and information about those SNPs including the position, and the test statistic across groups. 
3. Zoom-in and -out: Plotting many points on the same graph makes it difficult to discern one point from another, as it may be in a peak or in the lower portion of the Manhattan plot which often is densely packed. To overcome this issue, the plot can be zoomed-in using a mouse scroller when the mouse pointer is placed on the Manhattan plot.  

#### Visualization Sharing
Interactive plots can be saved as notebooks and self-contained html files that can be shared with colleagues via usual sharing platforms (GitHub, Dropbox, Google Drive, etc.) and opened in any modern web browsers on any operation system.

#### Limitations
In general, interactive visualization made through web browsers are limited by the number of objects they can smoothly display. To address this limitation, the package can be extended to a web application with dynamic data loading from a database/server. Dynamic data loading would allow a user to load SNP data in real time for a specific region of interest as the user zooms-in. By making this an open source package that is accessible via GitHub, we invite members of the scientific community to contribute and enhance the package’s capabilities. 

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

