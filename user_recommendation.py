import spacy
from collections import Counter
import traceback

#project module imports:
from clustering import get_dataset
from knowledge_graph import construct_knowledge_graph
import nlp_tasks as mynlp
import numpy as np
import pandas as pd
import scipy.stats
import gensim.downloader as api

nlp = spacy.load("en_core_web_lg")
model = api.load('word2vec-google-news-300')

#TOP_CATEG_COUNT = 3

def recommend_users(texts, user, user_knowledge_graph_df = None):
    print(user)
    user = int(user)
    vectors = {}
    index = 0
    for text in texts:
        try:
            for t in text:
                print("text", mynlp.remove_stop_words(t))
            user_knowledge_graph_df = construct_knowledge_graph(text)
            user_knowledge_graph_df['Combined Entities'] = user_knowledge_graph_df['Subjects and Objects'] + \
                                                        user_knowledge_graph_df['Entity List']
            print("know",user_knowledge_graph_df)

            entities = list(user_knowledge_graph_df['Combined Entities'])
            entities_joined = []
            for ent_list in entities:
                if len(ent_list) > 0:
                    txt = mynlp.remove_stop_words(' '.join(ent_list))
                    if len(txt) > 0:
                        entities_joined.append(txt)
            print("joined",entities_joined)

            df = get_dataset()
            #df = pd.read_csv('final_dataset.csv')
            categories = list(df['Type'].unique())

            text_docs = [nlp(ents) for ents in entities_joined]
            category_docs = [nlp(cat) for cat in categories]
            #print("text", text_docs)
            #print("cate",category_docs)

            max_score_details = []
            for doc in text_docs:
                sim_scores = []
                for i in range(len(category_docs)):
                    cat_doc = category_docs[i]
                    sim_scores.append((doc.similarity(cat_doc), doc.text, categories[i]))
                max_score_details.append(sorted(sim_scores, key=lambda x: x[0], reverse=True)[0])

            max_score_categories = [score[2] for score in max_score_details if score[0] > 0]
            counts = Counter(max_score_categories)
            count_tuples = list(counts.items())
            sorted_count_tuples = sorted(count_tuples, key=lambda x: x[1], reverse=True)
            categories_to_recommend = [tup[0] for tup in sorted_count_tuples[:]]

            # taking the max score text from each category to be recommended
            recom_req_dict = {}
            for categ in categories_to_recommend:
                recom_req_dict[categ] = []
            for detail in max_score_details:
                categ = detail[2]
                if categ in categories_to_recommend:
                    recom_req_dict[categ].append(detail)

            # keeping only the max score detail
            for key in recom_req_dict:
                detail = recom_req_dict[key]
                recom_req_dict[key] = max(detail, key=lambda x: x[0])[1]
            
            print("yuh",recom_req_dict)

            #using cluster predictions from the dataset to take the recommendations
            for categ in recom_req_dict:
                if categ not in vectors:
                    vectors[categ] = ['']*len(texts)
                vectors[categ][index] = recom_req_dict[categ]
            index += 1


        except Exception as e:
            print("Error occurred in the recommend_web_articles method: ", e, traceback.print_exc())
    print(vectors)
    matrix = []
    matrix_2 = []
    for a in range(len(texts)):
        print("categ ", categ)
        # for a in range(len(texts)):
        #     for b in range(len(texts)):
        #         if vectors[categ][a] != '' and vectors[categ][b] != '' and a != b:
        #             distance = model.wmdistance(vectors[categ][a], vectors[categ][b])
        #             print('distance = ', a, b, distance)
        user_arr = []
        for categ in vectors:
            if vectors[categ][a] != '' and vectors[categ][user] != '':
                distance = model.wmdistance(vectors[categ][a], vectors[categ][user])
                print('distance = ', a, user, distance)
            else:
                distance = 100.0
            user_arr.append(distance)
            matrix.append(distance)
        matrix_2.append(user_arr)
    print(matrix)
    print(np.array(matrix))
    print(pd.DataFrame(data = np.array(matrix).reshape(len(texts),len(vectors))))
    #matrix_2 = pd.DataFrame(data = np.array(matrix).reshape(len(texts),len(vectors)))
    print(matrix_2)

    sim_mat = np.array([similarity_pearson(matrix_2[i], matrix_2[j]) for i in range(0,len(texts)) for j in range(0,len(texts))])
    sim_df = pd.DataFrame(data = sim_mat.reshape(len(texts),len(texts)))
    print(sim_df)
    print(sim_df[user])
    print(sim_df[user].nlargest(2).index[1])

    return { "Most Similar User": str(sim_df[user].nlargest(2).index[1]) }

def similarity_pearson(x, y):
    return scipy.stats.pearsonr(x, y)[0]
