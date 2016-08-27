**Instagram_spider_application** 
============================================================

*This project contains of several examples of the usage of Instagram_spider*

Introduction of Instagram_spider
--------------------------------
It is a non-API Instagram spider, which has the following advantages:
1. Python 3.5: I am using python 3.5 to develop this spider. As Scrapy is still not fully supported for python 3.5 for now. If you want to do some crawling with python 3.5, you should try this out.
2. Non-API: Instead of using official API to access data, I choose to use the old-school way. Thus you don’t need to register as developer to use this library.
3. Fully-functional: Every data you can find from Instagram through browser, you can get access to it with this InstagramSpider. For instance, you can get access to all the data about the users, the hash tags as well as all the medias.
4. Highly-open: The Instagram_data library offers multiple functions to collect different data from the Instagram. You are free to use them for your own interest and develop your own program based on it.
You can find the resource through the following link:
https://github.com/panda0881/Instagram_data

Examples
--------
1. user_interest_analysis: analyzing the interest distribution of a specific user based on his/her post tags
2. tag_analysis: analyzing the overall interest distribution of people who are active under the specific tag
3. seed_user_searching: Using the result of user interest analysis to determine whether he fits the target profile or not. If the user fits the profile, we can take him as a potential seed user.
