import pandas as pd
import numpy as np
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from config import BOOKS_PATH, DB_PATH, EMBEDDING_MODEL, FALLBACK_COVER


class BookRecommender:
    def __init__(self):
        # Load dataset
        self.books = pd.read_csv(BOOKS_PATH)

        # Fix thumbnails
        self.books["large_thumbnail"] = self.books["thumbnail"] + "&fife=w800"
        self.books["large_thumbnail"] = np.where(
            self.books["large_thumbnail"].isna(),
            FALLBACK_COVER,
            self.books["large_thumbnail"],
        )

        # Load embeddings + DB
        embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
        self.db_books = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)

        # UI options
        self.categories = ["All"] + sorted(self.books["simple_categories"].unique())
        self.tones = ["All", "Happy", "Surprising", "Angry", "Suspenseful", "Sad"]

    def retrieve_recommendations(
        self,
        query: str,
        category: str = "All",
        tone: str = "All",
        initial_top_k: int = 50,
        final_top_k: int = 16,
    ) -> pd.DataFrame:
        recs = self.db_books.similarity_search(query, k=initial_top_k)
        books_list = [
            int(token.rstrip(":"))
            for rec in recs
            for token in [rec.page_content.strip('"').split()[0]]
            if token.rstrip(":").isdigit()
        ]

        book_recs = self.books[self.books["isbn13"].isin(books_list)].head(
            initial_top_k
        )

        # Category filtering with head(final_top_k) applied early
        if category != "All":
            book_recs = book_recs[book_recs["simple_categories"] == category].head(
                final_top_k
            )
        else:
            book_recs = book_recs.head(final_top_k)

        # Tone sorting (applied after limiting to 16)
        tone_column = {
            "Happy": "joy",
            "Surprising": "surprise",
            "Angry": "anger",
            "Suspenseful": "fear",
            "Sad": "sadness",
        }.get(tone)

        if tone_column:
            book_recs = book_recs.sort_values(by=tone_column, ascending=False)

        return book_recs

    def format_recommendations(self, recommendations: pd.DataFrame):
        """Format results for Gradio Gallery."""
        results = []

        for _, row in recommendations.iterrows():
            description = str(row.get("description", ""))
            words = description.split()
            truncated_description = " ".join(words[:30])
            if len(words) > 30:
                truncated_description += "..."

            # Format authors
            authors_split = [a.strip() for a in row["authors"].split(";")]
            if len(authors_split) == 2:
                authors_str = f"{authors_split[0]} and {authors_split[1]}"
            elif len(authors_split) > 2:
                authors_str = (
                    f"{', '.join(authors_split[:-1])}, and {authors_split[-1]}"
                )
            else:
                authors_str = authors_split[0] if authors_split else "Unknown"

            caption = (
                f"{row['title_and_subtitle']} by {authors_str}: {truncated_description}"
            )
            results.append((row["large_thumbnail"], caption))

        return results

    def recommend_books(self, query: str, category: str, tone: str):
        recs = self.retrieve_recommendations(query, category, tone)
        return self.format_recommendations(recs)
