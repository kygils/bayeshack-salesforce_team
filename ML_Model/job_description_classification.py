#pipeline that converts text to tfidf vectors and trains classification model based on
# Multinomial Naive Bayes model with a specified prior.
def build_model(X_train,Y_train,fit_prior):
    text_clf = Pipeline([('vect', CountVectorizer()),
                         ('tfidf', TfidfTransformer()),
                         ('clf', MultinomialNB(fit_prior=fit_prior)),])
    text_clf = text_clf.fit(X_train, Y_train)
    gs_clf = text_clf.fit(X_train, Y_train)
    return gs_clf

#helper function to classify new Craigslist postings
def classify_posting(model,cl_title,cl_description):
    
    test=cl_title+' '+cl_description
    return model.predict(test)

#function to clean text of extra symbols and stopwords
def clean_name(raw):
    letters=re.sub("[^a-zA-Z]", " ", raw)
    words=letters.lower().split()
    stops=set(stopwords.words("english"))
    meaningful=[w for w in words if not w in stops]
    return (" ".join( meaningful))

#function that was used to remove most common words in Craigslist job postings
#i.e. compensation, pay, equal opportunity, etc.
def remove_common(title,description):
    description=title+' '+description
    g=' '.join(description.values)
    h=Counter(g.split()).most_common()
    h_df=pd.DataFrame(h)
    takeout=h_df.loc[:50,].head(43)[0]
    test=[]
    for x in description:
        REMOVE_LIST=list(takeout)
        remove = '|'.join(REMOVE_LIST)
        regex = re.compile(r'\b('+remove+r')\b', flags=re.IGNORECASE)
        out = regex.sub("", x)
        test.append(out)
    return test