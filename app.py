from schema import UserGet, PostGet, FeedGet
from database import SessionLocal
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from fastapi import FastAPI, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from table_post import Post
from table_user import User
from table_feed import Feed
import os
import pickle
from datetime import datetime
import pandas as pd

SQLALCHEMY_DATABASE_URL = "postgresql://robot-startml-ro:pheiph0hahj1Vaif@postgres.lab.karpov.courses:6432/startml"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

Base = declarative_base()

app = FastAPI()



def get_db():
    with SessionLocal() as db: 
        return db




@app.get('/user/{id}', response_model=UserGet)
def user_get(id: int, db: Session = Depends(get_db)) -> UserGet:

    result = db.query(User).filter(User.id == id).one_or_none()

    if result is None:
        raise HTTPException(404, "user not found")
    else:
        return result


@app.get('/post/{id}', response_model=PostGet)
def post_get(id: int, db: Session = Depends(get_db)) -> PostGet:

    result = db.query(Post).filter(Post.id == id).one_or_none()

    if result is None:
        raise HTTPException(404, "user not found")
    else:
        return result
    

@app.get('/user/{id}/feed', response_model=List[FeedGet])
def get_actions(id: int, limit: int = 10, db: Session = Depends(get_db)):

    result = db.query(Feed).filter(Feed.user_id == id).order_by(Feed.time.desc()).limit(limit).all()

    return result
    


def get_model_path(path: str) -> str:
    if os.environ.get("IS_LMS") == "1":  
        MODEL_PATH = '/workdir/user_input/model'
    else:
        MODEL_PATH = path
    return MODEL_PATH

def load_models():
    model_path = get_model_path("/Users/artem/programming/ml/karpov_course/project_Ml_course/lesson_22_ml/XGBClassifier.pkl")
    model = pickle.load(open(model_path, 'rb')) 
    return model

model = load_models()

def load_features() -> pd.DataFrame:

    def batch_load_sql(query: str) -> pd.DataFrame:
        CHUNKSIZE = 200000
        engine = create_engine(
            "postgresql://robot-startml-ro:pheiph0hahj1Vaif@"
            "postgres.lab.karpov.courses:6432/startml"
        )
        conn = engine.connect().execution_options(stream_results=True)
        chunks = []
        for chunk_dataframe in pd.read_sql(query, conn, chunksize=CHUNKSIZE):
            chunks.append(chunk_dataframe)
        conn.close()
        return pd.concat(chunks, ignore_index=True)

    query = "SELECT * FROM artem_lesson_22_user_item_features"
    df = pd.DataFrame(batch_load_sql(query).drop(columns='index'))
    return df





user_data = pd.read_sql("SELECT DISTINCT ON (user_id) * FROM public.user_data", engine)
post_text_df = pd.read_sql('SELECT * FROM public.post_text_df', engine)

def make_predictions(id: int, user_data, post_text_df, model, num: int = 5):
   columns_order = ['user_id', 'post_id', 'gender', 'age', 'country', 'city', 'exp_group',
      'os', 'source', 'text', 'topic']

   result = pd.merge(user_data[user_data['user_id']==id].assign(key=1), post_text_df.assign(key=1), on='key').drop('key', axis=1)
   result = result[columns_order]
   
   preds = model.predict_proba(result)[:,1]

   final_df = pd.DataFrame({'post_id':result['post_id'],'prediction': preds})

   final_df = final_df.merge(post_text_df).sort_values(by='prediction', ascending=False)

   return final_df[:num]



@app.get("/post/recommendations/", response_model=List[PostGet])
def recommended_posts(
		id: int, 
		time: datetime = datetime.now(), 
		limit: int = 5) -> List[PostGet]:


    li = []
    df = make_predictions(id, user_data, post_text_df, model)
    for i in df.values:
        li.append(PostGet(id=i[0],text=i[2],topic=i[3]))
    
    return li

