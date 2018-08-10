# BillBoard_and_RIAA_datasets
Recent data sets created by scraping key Billboard Charts and RIAA Gold &amp; Platinum Certifications Lists

<h2>Introduction</h2>

Two of the key sources in tracking the volume of sales of songs and albums including the purchase of physical media, online downloads, and online streaming are Billboard and RIAA (short for the <i>Recording Industry Association of America</i>).  Billboard published its first music hit parade in 1936, its first popularity chart in 1940, and the current form of its consolidated Hot 100 in 1958. Similary, RIAA has been certifying Gold (500,000 units or over) since 1958 and Platinum unit sales (1 million or over) for both singles and albums since 1976. Over the years they have also introduced a couple of refinements to the platinum certifications including Multi-Platinum (multiples of one million units from 2X upward) and Diamond (those with 10 million or more unit sales).  They also started counting streaming units in 2011, although this requires conversion from streaming units to download sales.  The conversion for singles is "150 on-demand streams to 1 download sale"  and for albums it's 1,500 on-demand audio and/or video song streams = 10 track sales = 1 album sale. Their complete database is found at: https://www.riaa.com/gold-platinum/.

<h3>Charts and Reports Celebrating 60 Years: Billboard and RIAA</h3>

Both sources provide an extensive set individual charts and reports tracking various aspects of music sales. However, the focus here is on a set of charts and reports created in celebration of 60 years of operation - for Billboard it's 60 years for the Hot 100 and for RIAA it's 60 years of certifying gold and platinum sales volume.  These can be found at:

<ul>
<li> Billboard:<br>
<a href = "https://www.billboard.com/charts/hot-100-60th-anniversary"><b>Hot 100 60th Anniversary</b></a></li>
</li>
<li> RIAA:<br>
<a href = https://www.riaa.com/gold-platinum/?tab_active=awards_by_artist#search_section"><b>Certifications by Artists and Albums</b>   </a><br>
<a href = "https://www.riaa.com/gold-platinum/?tab_active=awards_by_artist#search_section"><b>Top Albums</b></a>
</li>
</ul>

Both sets of charts and reports only provide a starting point for creating the data sets of interest in this project. That is, additional pages and work are needed to create the final data sets. 

For a few reasons, the starting point for the Bill charts is further along than it is for the RIAA reports.

<ol> 
<li>The starting point for Billboard base data is a single page containing data on the Top 600 songs of all time including: song title, ranking, artist name, artist gender (female, male, duo/group), genre, and decade (of release).</li>
<li>The underlying source for the single Top 600 page provides html links to the <i>chart-history</i> pages for each artist. For example, the chart-history page for Chubby Checker is https://billboard.com/music/chubby-checker/chart-history. By the way, Chubby's song -- <i>The Twist</i> -- is the number 1 song of the last 60 years. Each artist's chart history page lists the number of number 1 songs, top 10 songs, and top 100 songs she, he or they have had over the years along with information about all their songs that have appeared on the charts (title, decade, highest ranking, etc.), although only up to 10 songs are automatically included on the chart-history page.</li>
<li>Other folks have created Python code for extracting the data from the Billboard charts.  The most prominent of these is a Python api called <i>Billboard.py</i> which was originally created by Allen Guo and is located on github at https://github.com/guoguo12/billboard-charts. It has been used in a number of other short studies which are listed in the readme of the repository. Unfortunately, it can't be directly used for extracting data from the Top 600 page and the associated chart-histories (mainly because they are not part of the regular Billboard charts).  Fortunately, the code does provide general pointers.
</ol>
 
While RIAA offers access to it's complete database, surfaces the means to query this database online, and provides immediate access to a some key standard queries (like Top Albums and Artists), there is no standard API for accessing the data. More important is the fact that any query only displays the first 30 rows of the result. If there are more than 30 rows, then a button will appear at the bottom of the page for loading the next 30 rows, and the next 30 rows,  and so on.  It takes one query and 3 button pushes to get to a 100+ rows. The frustrating part is that the page's underlying html source code only includes information about the first 30, not about subsequent panels even though the cumulative results are shown on the screen. The end result was that for all the RIAA datasets, I had to go through a number of button pushes to create the results on the screen and then manually highlight and copy the screen output to the clip board and then copy the clipped text to a text editor where I saved the text to a file.  I then scraped this file for the data of interest. Time consuming and tedious to say the least. 

<h3>Resulting Datasets</h3>

To date, the end result is 5 csv files - 2 based on the Billboard charts and 3 on RIAA data. These are provided in this respository and briefly described below:

<ul>
<li>
