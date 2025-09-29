from recommender import BookRecommender
from ui import BookRecommenderUI


if __name__ == "__main__":
    recommender = BookRecommender()
    ui = BookRecommenderUI(recommender)
    ui.launch()
