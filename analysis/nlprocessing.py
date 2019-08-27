import pandas as pd

def top_wgts(doc_tops, names, idx):
    top_df = pd.DataFrame(doc_tops)
    top_df.columns = top_df.columns.map(names)
    top_df.set_index(idx, inplace=True)
    return(top_df)

# function to print top words of topic model
def print_top_words(model, feature_names, n_top_words):
    for index, topic in enumerate(model.components_):
        message = "\nTopic #{}:".format(index)
        message += " ".join([feature_names[i] for i in topic.argsort()[:-n_top_words - 1 :-1]])
        print(message)
        print("="*70)
