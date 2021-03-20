def parse_monthly_json(file_path):
    """takes monthly json file paths and returns dataframe with text/metadata of interest"""
    import json
    import pandas as pd

    # parse the monthly json file that was downloaded
    with open(file_path) as json_file:
        parsed = json.load(json_file)

    # initialise collection of desired data items
    pub_date = []
    headline = []
    abstract = []
    news_desk = []
    section_name = []

    # iterate through all articles in the month and select data items of interest
    for article in parsed['response']['docs']:
        pub_date.append(article['pub_date'])  # publication date
        headline.append(article['headline']['main'])  # TEXT: headline
        abstract.append(article['abstract'])  # TEXT: short summary of article content
        news_desk.append(article['news_desk'])  # news desk that published the article
        section_name.append(article['section_name'])  # section in which article appeared

    return (pd.DataFrame({'pub_date': pub_date, 'headline': headline, 'abstract': abstract,
                          'news_desk': news_desk, 'section_name': section_name}))


def generate_tokens(args):
    """generates n-gram tokens from large dataframe covering all months
        takes the following arguments: the dataframe, the desired n-gram range
        (e.g. all 1-2 grams), minimum token count, and whether to apply
        a tfidf transform"""

    import numpy as np
    from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
    from scipy import sparse
    from scipy.io import mmwrite
    import feather
    import pandas as pd

    # parse arguments provided as list (this is neccesary for parallelisation)
    df = args[0]
    min_n = args[1]
    max_n = args[2]
    min_df = args[3]
    tfidf = args[4]

    # initialise vectoriser, depending on whether tfidf transform is desired
    if tfidf:
        vectorizer = TfidfVectorizer(ngram_range=(min_n, max_n), min_df=min_df)
    else:
        vectorizer = CountVectorizer(ngram_range=(min_n, max_n), min_df=min_df)

    # vectorise the article abstract text and collect token identities
    X = vectorizer.fit_transform(df.abstract)
    names = vectorizer.get_feature_names()

    # sum token counts for each month
    res = []
    unique_months = df.year_month.unique()
    unique_months = np.sort(unique_months)
    for month in unique_months:
        res.append(sparse.csr_matrix(X[df.year_month == month].sum(axis=0)))
    m_counts = sparse.vstack(res)

    # write ngrams to file, with filename indicating the chosen parameters (feather format is chosen for portability)
    mmwrite("processed_text/ngram_from_{}_to_{}_min_{}_tfidf_{}.mtx".format(min_n, max_n, min_df, tfidf), m_counts)

    # write ngram months to file (feather format is chosen for portability)
    pd.DataFrame({"year_month": unique_months}).to_feather(
        "processed_text/month_from_{}_to_{}_min_{}_tfidf_{}.feather".format(min_n, max_n, min_df, tfidf))

    # write ngram token identities to file (feather format is chosen for portability)
    pd.DataFrame({"feature": names}).to_feather(
        "processed_text/features_from_{}_to_{}_min_{}_tfidf_{}.feather".format(min_n, max_n, min_df, tfidf))
