# How it Works

## Step 1 | Spider the Website by running 'main.py'

- Spider the Website of your choice.
    - This algorithm won't wander away from the inputted website. For ex if the domain is 'www.wikipedia.org' then it will stay on 'www.wikipedia.org'.

- Grab all the links from the page, then randomly select a link, open the link and get all the links from that newly opened page.

- The above process goes on until the specified number of pages are retrieved. 

## Step 2 | Calculate Pageranks by running 'pagerank.py'

- After spidering has finished, calculate the page ranks of the retrieved pages. 

## Step 3 | Create JSON file using the links and ranks by running 'createJson.py'

- Generate a JSON file to help with D3JS visualization.

## Step 4 | Create a visualization using 'view.js' and view by opening 'view.html'

- All you have to do after the first three steps is to open 'view.html' to view the results.


### Step 1

![Spidering](https://i.ibb.co/20JnG1r/spidering.jpg)


### Steps 2 and 3

![Next-Steps](https://i.ibb.co/sFGHMWF/next-steps.jpg)

### Visual

![Graph](https://i.ibb.co/WP19N26/Graph-viz.jpg)