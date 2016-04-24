##Providing intelligent labor market data and applications to low and middle skill workers

As technological advances continue to permeate the economy, occupational and geographic communities must effectively bridge skill gaps that are inherently created in the labor market. 

Today, there are many intelligent platforms that connect high skill workers to potential employers, professional networks, and other occupations. However, the current data and tools available to low/middle skill workers are limited. Federal and state policymakers can do more to collect richer labor market data from the internet and incorporate simple machine learning models into existing platforms that personalize labor market tools for low/middle skill workers. With more data and intelligent tooling, the DOL can develop deeper insights into the labor market and labor market participants can greatly benefit from more customized applications. 

To illustrate how unstructured labor market data can be combined with existing labor market data, we developed an engine that pulls job postings from Craigslist and classifies them into standard government occupational codes. Not only are occupation/skill forecasts enhanced with finer grain data, but the same classification engine can also be leveraged in existing government applications to personalize job searches and optimize resources for low/middle skill workers. 

This model can be quickly integrated into the existing O*NET web application in a number of ways:

**1. Related occupations tool:** Currently, related occupations are static and are linked only between occupation codes. Our model can intake a resume or an unstructured block of text that describes an individual's job experience/skills/etc. and return a list of most related occupations. Our approach is personalized, drawing on the individual’s skills, experiences, background as opposed to only the job title/occupation code.

**2. Occupation growth forecasts based on real job postings:** Currently, the job forecasts posted on O*NET are static and based on a single study. With our collection and classification of job posting, we are able to provide dynamic growth rates of occupations and skills by geography. In addition, individuals can continue to leverage existing government resources associated with specific occupation codes. 

While examining the complex dynamics of large economic adaptation requires collecting and structuring vast amounts of labor related data from the internet, this model provides a practical first step towards serving low/middle skill workers with customized labor market resources. 
<hr>
#Project Components:
**1. Craigslist Job Scraper (iPython notebook):** code that scrapes today's job postings from Craigslist

**2. ML Model (Scikit Learn):** machine learning model that takes a string of words and returns job recommnedations

**3. Web App (Heroku/Flask):** web application deployed on Heroku that deomstrates a use case of the engine. In this web app, a user can upload a resume or describes their experience/skills, and the app will recommend personalized occupations. In addtion, the app will map related, Craigslist job postings with posting links. 
<hr> 

Technology Stack 
* Jupyter 
* Flask
* Scikit Learn
* Postgresql
* Heroku