# Pi-star Skyblazers 2020 TAMIDS Data Science Competition

This repo contains the solution of the team Pi-star Skyblazers that won the 1st place in the graduate division of the [2020 TAMIDS Data Science Competition](https://tamids.tamu.edu/2020/02/10/2020-data-science-competition-call/). The goal of this competition was to use airline data from the US Bureau of Transportation Statistics to develop performance measures for airlines and models to forecast expected performance. [Sumedh]() was my teammate in this project.

My team also stood 1st in the [2019 TAMIDS Data Science Competition](https://tamids.tamu.edu/2019/05/09/2019-tamids-data-science-competition-results/) during which I was part of a super-duper team.    

Below is a bird's eyeview of our approach and results. Please feel free to go through our [report]() for a detailed description of our approach, results, and findings. Much of the tips and tricks used in this project were from Jeremy Howard's [Intro to ML for Coders course](http://course18.fast.ai/ml.html). This course along with the [fastai](https://github.com/fastai/fastai) library are some of the best resources you can find on the web for free to slay most of your data science projects. Kudos to the team at Fast AI for their amazing efforts towards democratizing machine learning.  

## Goals
1. Predicting departure delays given the origin airport, destination airport, airline, date of travel, and time of departure.
2. Determining the main factors contributing towards flight delays.
3. Creating a web application in which a user can provide information regarding her planned travel and obtain an estimate of the flight delay.

## Approach

1. We visualized the data, with various charts, graphs, to get an overall overview of the data.
2. We found patterns from the observations and plots, and analyzed the importance of each feature on the delays to greater depth.
3. We used tree-based machine learning models such as random forests and gradient-boosted trees to predict flight delays.
4. We analyzed the importance of features to identify their amount of contribution to our predictions.
5. Using tree interpreters and waterfall charts we identif how different features impact our model’s prediction of delays.
6. We used partial dependence plots to analyze the impact of individual features, and feature interactions on delays.

## Delay Prediction

Our trained random forest model predicts an interval in which the delay for a particular flight might fall. Specifically, it provides a distribution over the delay intervals. The interval of the delays is 15 minutes and the minimum delay predicted is -30 minutes i.e the flight leaves before time while delays greater than 180 minutes have been grouped into a single interval block. We obtained a test accuracy of 62% :frowning_face: on about 100,000 trips. We believe that the low accuracy is due to the class imbalance present in the data since only about 20% trips are ones that were delayed. Shown below is the confusion matrix on the test data.  

![Confusion-matrix](/figures/confusion-matrix.png)

The plot below is the feature importance plot obtained from our model which quantifies the effect of each feature in our model on its predictions. It suggests that the day of the month and day of the week in which a flight departs, the number of passengers in the flight, and the flight number are the most important factors contributing towards flight delays. An interesting feature is the net income for the current year, month, route and carrier which may not be so obvious to a non-expert in this domain. This finding particularly emphasizes the significance of machine learning models to find minute non-obvious patterns in the data as the relationship between delays and net income is tough capture using just visualizations and heuristics.  

![Feature-importance](/figures/feature-importance.png)

The plot for the prediction probability distribution for a given sample trip is shown below.

![Preds](/figures/prediction-probs.png)

## Tree Interpretation

The waterfall chart below shows the contribution of each of the features of the sample trip on the final probability value in the (-15 - 0) minutes interval. The features with green bars are those which are helping the flight stay on time and while the ones with red bars are those which are doing the opposite. The left most green bar is the average prediction of our model.  

![Waterfall](/figures/waterfall-chart.png)

## Web Application

Below is a screenshot of our web-app. It allows you to look for the flight based on the source, destination, flight date, time of departure, and carrier. It shows you the expected delay, if any, and how likely it is. It also shows what works in your favour for the flight to be on time and what hurts. If you are on a tigher schedule for example, consider a vacation when you have less time between the flight and event, this might help you to consider another flight to avoid last minute rush as you plan your itinerary.  

![Web-app](/figures/web-app.png)

## Future Work

- [ ] Refactor code to make the testing pipeline lighweight
- [ ] Train a model taking into account the class imbalance problem in the dataset. Refer to [this](https://machinelearningmastery.com/bagging-and-random-forest-for-imbalanced-classification/).
- [ ] Find a place for hosting our web app for free