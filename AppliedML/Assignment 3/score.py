import pandas as pd
import joblib

def transform_df(df):
    """Pipeline to implement vectorization and tf-idf transformation"""

    pipeline = joblib.load('pipeline.pkl')
    
    corpus = df.text.values
    corpus_tfidf = pipeline.transform(corpus)

    df.reset_index(drop=True, inplace=True)
    df_transform = pd.concat([df, pd.DataFrame(corpus_tfidf.toarray())], axis=1)
    df_transform.drop('text', axis=1, inplace=True)

    return df_transform

def score(text:str, threshold:float = 0.5):

    df = pd.DataFrame([text], columns=['text'])
    df_transform = transform_df(df)
    df_transform.columns = df_transform.columns.astype(str)

    model = joblib.load('svc.pkl')
    pred_proba = model.predict_proba(df_transform)[0,1]
    
    assert type(text) == str
    assert ((type(threshold) == float) or type(threshold) == int) and (0 <= threshold <= 1)

    if pred_proba >= threshold:
        prediction = 1
    else:
        prediction = 0
    
    return prediction, pred_proba

if __name__ == "__main__":
    score("Hi, I will call you later, best regards")