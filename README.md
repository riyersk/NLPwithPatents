# NLPwithPatents
Exploring doc2vec with patent abstracts

For this project, I parsed patents from text files offered as bulk data downloads by the U.S. Department of Commerce.  I mapped the patent abstracts to 300 dimensional vectors using gensim's doc2vec, clustered the vectors from the year 2000 using dbscan, and visualized them using TSNE.

Guide to the code:

pats.py: This script is the code for a spider class that finds all the urls containing the downloadable text files.

patlist.py: This script contains the python code to take all the urls found by the pats.py spider, download the text file from each, and parse the patents in each textfile into a mongo database.

patdocs.py: This script contains the python code to generate doc2vec vectors for the abstracts and summaries of the patents in the mongo database.  It also saves the application dates and patent numbers of the corresponding patents to the disk in pickle objects.

showabvecs.ipynb: This python notebook file contains the code to cluster a subset of the abstract vectors (those with application dates in the year 2000), using DBSCAN, and then visualize those vectors using TSNE.
