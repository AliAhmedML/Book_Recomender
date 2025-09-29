import gradio as gr


class BookRecommenderUI:
    def __init__(self, recommender):
        self.recommender = recommender

    def launch(self):
        with gr.Blocks(theme=gr.themes.Glass()) as dashboard:
            gr.Markdown("# Semantic book recommender")

            with gr.Row():
                user_query = gr.Textbox(
                    label="Please enter a description of a book:",
                    placeholder="e.g., A story about forgiveness",
                )
                category_dropdown = gr.Dropdown(
                    choices=self.recommender.categories,
                    label="Select a category:",
                    value="All",
                )
                tone_dropdown = gr.Dropdown(
                    choices=self.recommender.tones,
                    label="Select an emotional tone:",
                    value="All",
                )
                submit_button = gr.Button("Find recommendations")

            gr.Markdown("## Recommendations")
            output = gr.Gallery(label="Recommended books", columns=8, rows=2)

            submit_button.click(
                fn=self.recommender.recommend_books,
                inputs=[user_query, category_dropdown, tone_dropdown],
                outputs=output,
            )

        dashboard.launch()
