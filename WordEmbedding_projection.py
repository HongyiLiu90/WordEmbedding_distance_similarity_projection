#!/usr/bin/env python
# -*- coding: utf-8 -*-



###----------Word2Vec, fastText, and GloVe analysis-----------####



# Hongyi Liu
# Dept. of Economics, WashU
# Sep. 10, 2018


import os, sys, fnmatch, csv, codecs
from gensim.models import KeyedVectors
from scipy.spatial.distance import cosine



# parametization

language, model = sys.argv[1:3]

root = '/scratch/Users/GoogleBooks'   # given the root



# computing the distance and similarity between two words

def dist_simi(word1, word2, word_vectors, vocab):  # word1 & word2 are strings, word_vectors & vocab are varname
    if (word1 in vocab) & (word2 in vocab):
        dist = word_vectors.distance(word1, word2)
        dist = float("{:.2f}".format(dist)) # limiting to two decimals
        similarity = word_vectors.similarity(word1, word2)
        similarity = float("{:.2f}".format(similarity)) # limiting to two decimals
        return dist, similarity
    else:
        dist, similarity = None, None
        return dist, similarity

# computing the cosine similarity among three words
def cos_simi(word, post, nega, word_vectors, vocab):
    if (word in vocab) & (post in vocab) & (nega in vocab):
        cos_simi = word_vectors.most_similar(positive=[post, word], negative=[nega], topn=1)
        cos_simi = "{}: {:.4f}".format(*cos_simi[0]) # limiting to four decimals
        return cos_simi
    else:
        cos_simi = None
        return cos_simi

# computing the most similar word
def most_similar(word, post, nega, word_vectors, vocab):
    if (word in vocab) & (post in vocab) & (nega in vocab):
        most_similar = word_vectors.most_similar_to_given(word, [post, nega])
        #cos_proj = "{}: {:.4f}".format(*cos_proj[0]) # limiting to four decimals
        return most_similar
    else:
        most_similar = None
        return most_similar


# computing the cosine projection of one word onto two words
def cos_proj(word, post, nega, word_vectors, vocab):
    if (word in vocab) & (post in vocab) & (nega in vocab):
        vector = word_vectors[word]
        post_nega = word_vectors[post] - word_vectors[nega]
        cos_proj = 1-cosine(vector, post_nega)
        cos_proj = "{:.4f}".format(cos_proj)

        return cos_proj
    else:
        cos_proj = None
        return cos_proj

# computing the cosine similarity of two dimisions
def cos_dim(word1, word2, post, nega, word_vectors, vocab):
    if (word1 in vocab) & (word2 in vocab) & (post in vocab) & (nega in vocab):
        cos_dim = word_vectors.n_similarity([word1, word2], [post, nega])
        cos_dim = "{:.4f}".format(cos_dim) # limiting to four decimals
        return cos_dim
    else:
        cos_dim = None
        return cos_dim

# output the results
def export_results(outcome, path, Title):
    if not os.path.exists(path):
        with open(path,'w',encoding='utf-8-sig') as result:
            #result.write(codecs.BOM_UTF8)
            writer = csv.writer(result, delimiter=',')
            writer.writerow(Title)
            writer.writerow(outcome)
        result.close()
    # append to the existing csv file
    else:
        with open(path,'a',encoding='utf-8-sig') as result:
            #result.write(codecs.BOM_UTF8)
            writer = csv.writer(result, delimiter=',')
            writer.writerow(outcome)
        result.close()

        
# build up the dictionary for different words in different languages.


bank_all = {'chi': '银行', 'eng':'bank', 'fre': 'banque', 'spa': 'banco',
           'ger': 'bank', 'rus': 'банк', 'ita': 'banca', 'heb': 'בנק'}

banking_all = {'chi': '银行业', 'eng':'banking', 'fre': 'bancaire', 'spa': 'bancario',
           'ger': 'bankenwesen', 'rus': 'банковское дело', 'ita': 'bancario', 'heb': 'בנקאות'}

investment_all = {'chi': '投资', 'eng':'investment', 'fre': 'investissement', 'spa': 'inversión',
           'ger': 'investition', 'rus': 'инвестиции', 'ita': 'investimento', 'heb': 'השקעה'}

stock_all = {'chi': '股票', 'eng':'stock', 'fre': 'stock', 'spa': 'valor',
           'ger': 'aktie', 'rus': 'акции', 'ita': 'azione', 'heb': 'מניה'}

corporate_all = {'chi': '公司', 'eng':'corporate', 'fre': 'entreprise', 'spa': 'corporativo',
           'ger': 'unternehmen', 'rus': 'корпоративный', 'ita': 'aziendale', 'heb': 'תאגיד'}

good_all = {'chi': '好', 'eng':'good', 'fre': 'bien', 'spa': 'bueno',
           'ger': 'gut', 'rus': 'хороший', 'ita': 'bene', 'heb': 'טוב'}

bad_all = {'chi': '坏', 'eng':'bad', 'fre': 'mal', 'spa': 'malo',
           'ger': 'schlecht', 'rus': 'плохой', 'ita': 'cattivo', 'heb': 'רע'}

capitalism_all = {'chi': '资本主义', 'eng':'capitalism', 'fre': 'capitalisme', 'spa': 'capitalismo',
           'ger': 'kapitalismus', 'rus': 'капитализм', 'ita': 'capitalismo', 'heb': 'קפיטליזם'}



path = root + '/' + model + '/' + language
os.chdir(path)
if os.path.exists('.DS_Store'):
    os.remove('.DS_Store')  # in ios system, there exists a file named .DS_Store indicating the attribute of each folder
else:
    pass
file = (tr for tr in os.listdir(path) if tr not in fnmatch.filter(os.listdir(path), "*.*"))
for f in file:
    key = f.split('-',1)[0]
    yr = int(f.split('-')[-1])
    finance, bank, banking = finance_all[key], bank_all[key], banking_all[key]
    capitalism, stock = capitalism_all[key], stock_all[key]
    investment, corporate = investment_all[key], corporate_all[key]
    good, bad = good_all[key], bad_all[key]
    result_path = root + '/' + model + '/'+ language +'/'+ language + '_' + model +'.csv'
    columnTitleRow = [language ,'dist_bank_good', 'similarity_bank_good','dist_bank_bad', 'similarity_bank_bad',
                         'dist_good_bad', 'similarity_good_bad', 'dist_bank_invest', 'similarity_bank_invest',
                        'dist_bank_stock', 'similarity_bank_stock', 'dist_bank_corp', 'similarity_bank_corp',
                          'analogy_bank','analogy_banking', 'analogy_capit', 'analogy_invest',
                        'analogy_stock', 'analogy_corp','cos_proj_bank','cos_proj_banking', 'cos_proj_capit',
                        'cos_proj_invest', 'cos_proj_stock', 'cos_proj_corp']

    if model in {'Word2Vec', 'GloVe'}:
        word_vectors = KeyedVectors.load(f, mmap='r')
        vocab = word_vectors.vocab

    if model in {'fastText'}:
        m = KeyedVectors.load(f, mmap='r')
        word_vectors = m.wv
        vocab = m.wv.vocab
            # check if the words target words exist and compute the corresponding distance, similarity, and cosine similarity

            # computing distance and similarity


    dist_bank_good, similarity_bank_good = dist_simi(bank, good, word_vectors, vocab)
    dist_bank_bad, similarity_bank_bad = dist_simi(bank, bad, word_vectors, vocab)
    dist_good_bad, similarity_good_bad = dist_simi(good, bad, word_vectors, vocab)


    dist_bank_invest, similarity_bank_invest = dist_simi(bank, investment, word_vectors, vocab)
    dist_bank_stock, similarity_bank_stock = dist_simi(bank, stock, word_vectors, vocab)
    dist_bank_corp, similarity_bank_corp = dist_simi(bank, corporate, word_vectors, vocab)



    analogy_bank = cos_simi(bank, good, bad, word_vectors, vocab)
    analogy_banking = cos_simi(banking, good, bad, word_vectors, vocab)
    analogy_capit = cos_simi(capitalism, good, bad, word_vectors, vocab)
    analogy_invest = cos_simi(investment, good, bad, word_vectors, vocab)
    analogy_stock = cos_simi(stock, good, bad, word_vectors, vocab)
    analogy_corp = cos_simi(corporate, good, bad, word_vectors, vocab)




    cos_proj_bank = cos_proj(bank, good, bad, word_vectors, vocab)
    cos_proj_banking = cos_proj(banking, good, bad, word_vectors, vocab)
    cos_proj_capit = cos_proj(capitalism, good, bad, word_vectors, vocab)
    cos_proj_invest = cos_proj(investment, good, bad, word_vectors, vocab)
    cos_proj_stock = cos_proj(stock, good, bad, word_vectors, vocab)
    cos_proj_corp = cos_proj(corporate, good, bad, word_vectors, vocab)

                # write results to csv file
    row = [yr, dist_bank_good, similarity_bank_good, dist_bank_bad, similarity_bank_bad, dist_good_bad, similarity_good_bad,
            dist_bank_invest, similarity_bank_invest, dist_bank_stock, similarity_bank_stock,dist_bank_corp, similarity_bank_corp,
            analogy_bank, analogy_banking, analogy_capit, analogy_invest, analogy_stock, analogy_corp,
            cos_proj_bank, cos_proj_banking, cos_proj_capit, cos_proj_invest, cos_proj_stock, cos_proj_corp, ]


    export_results(row, result_path, columnTitleRow)
