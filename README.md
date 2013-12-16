Yolanda Info Classifier
=======================
Social media has made it easier to relay information regarding the Haiyan/Yolanda rescue effort. Although this has been very helpful, there is now so much information with very varied content that it has become difficult to sift through. The goal of this project is to use a mix of crowdsourcing and machine learning to categorize information.

Contributors will manually categorize information using a web interface so that users can then view messages according to their categories. In the background, a machine learner will use the manually labeled categories so it can automate the categorization of other information. This is necessary especially because of the volume of information produced.

An initial version of the project can be accessed here: http://yolanda-oshakathon.rhcloud.com/
The APIs for retrieving information categories are made available so that other projects can leverage on them. Information regarding the APIs can be found here: http://yolanda-oshakathon.rhcloud.com/api.html

Requirements
------------
1. Gevent - http://www.gevent.org/
2. TwitterAPI - https://github.com/geduldig/TwitterAPI
3. redis-py - https://github.com/andymccurdy/redis-py
4. Scikit Learn - http://scikit-learn.org/
