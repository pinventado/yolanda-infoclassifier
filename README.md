Yolanda Info Classifier
=======================
Social media has made it easier to relay information regarding the Haiyan/Yolanda rescue effort. Although this has been very helpful, there is now so much information with very varied content that it has become difficult to sift through. The goal of this project is to use a mix of crowdsourcing and machine learning to categorize information.

Contributors will manually categorize information using a web interface so that users can then view messages according to their categories. In the background, a machine learner will use the manually labeled categories so it can automate the categorization of other information. This is necessary especially because of the volume of information produced.

The API for retrieving information categories will be made available so that other projects can leverage on them.

Requirements
------------
1. TwitterAPI - https://github.com/geduldig/TwitterAPI
2. redis-py - https://github.com/andymccurdy/redis-py
3. Scikit Learn - http://scikit-learn.org/
