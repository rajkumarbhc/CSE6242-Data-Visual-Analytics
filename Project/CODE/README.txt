DESCRIPTION
1. dataCollection.py
    This Python script uses Twitter's Streaming API to collect real-time tweets containing the keywords (stored in the four files in the 'keywords' folder). It requires Tweepy package and you need to provide a key file (in the 'keysAuth' folder) for API authorization. The output files will be automatically placed in the 'output' folder.

2. dataAnalysis.py
    This Python script is used for data post-processing and analysis for the collected tweets. It requires vaderSentiment package to perform sentiment analysis. The code should be self-explanatory.

3. dataAnalysisHelper.py
    This Python script contains a few helper functions for data post-processing.

4. dataVisualization
    This folder contains all necessary files for visualizing our results. The main executable codes are the two HTML files (i.e., visualization_Percent_SI.html and visualization_top_disease.html).


INSTALLATION
Our package does not require installment.


EXECUTION
1. To execute dataCollection.py, simply run the following command:
        python dataCollection.py

2. To execute dataAnalysis.py, simply run the following command:
        python dataAnalysis.py

3. To visualize our results, simply open the HTML file in the browser (chrome and Firefox are recommended). Note a local server is required to show the webpage.