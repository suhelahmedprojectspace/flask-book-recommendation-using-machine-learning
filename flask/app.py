    #getting the details for authors
    #getting the details for authors
import numpy as np
import pandas as pd
from flask import Flask, render_template, request,redirect,url_for
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.neighbors import NearestNeighbors

import requests


 
app=Flask(__name__)  

def create_model():
    #import dataset
    data = pd.read_csv('C:/Users/suhel/Desktop/book recommendation/file.csv')
    # create count matrix
    cv = CountVectorizer()
    count_matrix = cv.fit_transform(data['title'])
    # create similarity score matrix
    model = NearestNeighbors(metric='cosine', algorithm='brute')
    model.fit(count_matrix)
    return data, model, count_matrix


def recommend(choice):
    
    try:
        model.get_params()
    except:
        data, model, count_matrix = create_model()
        #distances,indices = model.kneighbors(count_matrix[choice_index],n_neighbors=11)

    if choice in data['title'].values:
        choice_index = data[data['title'] == choice].index.values[0]
        distances, indices = model.kneighbors(
            count_matrix[choice_index], n_neighbors=9)
        book_list = []
        for i in indices.flatten():
            book_list.append(data[data.index == i]
                              ['title'].values[0].title())
                        
        return book_list 

    elif (data['title'].str.contains(choice).any() == True):

        # getting list of similar book names as choice.
        similar_names = list(str(s) for s in data['title'] if choice in str(s))
        # sorting the list to get the most matched book name.
        similar_names.sort()
        # taking the first book from the sorted similar books name.
        new_choice = similar_names[0]
        print(new_choice)
        # getting index of the choice from the dataset
        choice_index = data[data['title'] == new_choice].index.values[0]
        # getting distances and indices of 16 mostly related movies with the choice.
        distances, indices = model.kneighbors(
            count_matrix[choice_index], n_neighbors=9)
        # creating book list
        book_list = []
        for i in indices.flatten():
            book_list.append(data[data.index == i]
                              ['title'].values[0].title())                                        
        return book_list
    else:
        return redirect(url_for('error'))



# getting the image list        

def get_image(choice):
    try:
        model.get_params()
    except:
        data, model, count_matrix = create_model()
        #distances,indices = model.kneighbors(count_matrix[choice_index],n_neighbors=11)

    if choice in data['title'].values:
        choice_index = data[data['title'] == choice].index.values[0]
        distances, indices = model.kneighbors(
            count_matrix[choice_index], n_neighbors=9)

        img_list=[]    
        
        for i in indices.flatten():
            img_list.append(data[data.index == i]
                              ['Image'].values[0])
                        
        return img_list 

    elif (data['title'].str.contains(choice).any() == True):

        # getting list of similar book names as choice.
        similar_names = list(str(s) for s in data['title'] if choice in str(s))
        # sorting the list to get the most matched book name.
        similar_names.sort()
        # taking the first book from the sorted similar books name.
        new_choice = similar_names[0]
        
        # getting index of the choice from the dataset
        choice_index = data[data['title'] == new_choice].index.values[0]
        # getting distances and indices of 16 mostly related movies with the choice.
        distances, indices = model.kneighbors(
            count_matrix[choice_index], n_neighbors=9)
        # creating book image list
        img_list=[]
        for i in indices.flatten():
            img_list.append(data[data.index == i]
                              ['Image'].values[0])
                                                    
        return img_list

    else:
        return redirect(url_for('error'))




#getting details from google books api
def get_book_details(title):
    book_details=[]
    url='https://www.googleapis.com/books/v1/volumes?q='
    name=str(title)
    response=requests.get(url + name)
    obj=response.json()
    try:
        author = obj["items"][0]["volumeInfo"]["authors"]
        book_details.append(author)
        des = obj["items"][0]["volumeInfo"]["description"]
        book_details.append(des)
        average = obj["items"][0]["volumeInfo"]["averageRating"]
        book_details.append(average)
        return book_details
    except:
          pass
     
#getting books by details 
def get_name_by_author(name):
    data=pd.read_csv('C:/Users/suhel/Desktop/book recommendation/file.csv')
    w=data[data['author']==name]
    title=w['title'].tolist()
    return title
    
def get_rating_by_author(name):
    data=pd.read_csv('C:/Users/suhel/Desktop/book recommendation/file.csv')
    w=data[data['author']==name]
    rating=w['rating'].tolist()
    return rating

def get_isbn_by_author(name):
    data=pd.read_csv('C:/Users/suhel/Desktop/book recommendation/file.csv')
    w=data[data['author']==name]
    no=w['rating'].tolist()
    return no
    
@app.route('/error')
def error():
    return render_template('404.html')

    
@app.route('/')
def home():
    return render_template('Home.html')

@app.route('/filter',methods=['GET','POST'])
def fi():
    return render_template('filter.html', data=[{'name':'Danielle Steel'},{'name':'Richard Laymon'},{'name':'Nora Roberts'}],
    data2=[{'name':'JOHN GRISHAM'},{'name':'Tom Clancy'},{'name':'PHILIP PULLMAN'}],data3=[{'name':'J. K. Rowling'},{'name':'Stephen King'},{'name':'Sandra Brown'}])
      
@app.route('/filter_take',methods=['GET','POST'])
def filter_take():
    choice1=request.form.get('choice1')
    choice2=request.form.get('choice2')
    choice3=request.form.get('choice3')
    #getting the details for author
    book1_name=get_name_by_author(choice1)
    book1_rating=get_rating_by_author(choice1)
    book1_isbn=get_isbn_by_author(choice1)
    #getting the details for authors
    book2_name=get_name_by_author(choice2)
    book2_rating=get_rating_by_author(choice2)
    book2_isbn=get_isbn_by_author(choice2)

    #getting the details for authors 3
    book3_name=get_name_by_author(choice3)
    book3_rating=get_rating_by_author(choice3)
    book3_isbn=get_isbn_by_author(choice3)
    print(book3_isbn)
    return render_template('display.html',choice1=choice1,choice2=choice2, choice3=choice3,
    book1_name=book1_name,book1_rating=book1_rating,book1_isbn=book1_isbn,book2_name=book2_name, book2_rating=book2_rating,book2_isbn=book2_isbn,book3_name=book3_name, book3_rating=book3_rating,book3_isbn=book3_isbn)

@app.route('/search',methods=['GET','POST'])
def search():
    choice = request.args.get('search')
    # removing all the characters except alphabets and numbers.
    # passing the choice to the recommend() function
    # passing the choice to the get_image() function
    books = recommend(choice)
    image=get_image(choice)
    print(image)
    # if rocommendation is a string and not list then it is else part of the
    # recommend() function.
    if type(books) == type('string'):
        return render_template('read.html', book=books,image=image,s="oppps")
    else:
        return render_template('read.html', book=books,image=image)

@app.route('/bar',methods=['GET','POST'])
def bar():
     return render_template('search.html')

@app.route('/info',methods=['POST'])
def info():
    if request.method == "POST":
        title = request.form.get('results')
        book_image=request.form.get('l')
        details=get_book_details(title)   
        return render_template('info.html',title=title,details=details,book_image=book_image)
        
   


if __name__ =="__main__":
    app.run(debug=True)  
