import streamlit as st
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from typing import List, Optional
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel
from langchain_mistralai import ChatMistralAI

# Load environment variables
load_dotenv()


# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Movie Information Extractor",
    page_icon="🎬",
    layout="centered"
)


# -----------------------------
# Pydantic Model
# -----------------------------
class Movie(BaseModel):
    title: str
    release_year: Optional[int] = None
    genre: List[str]
    director: Optional[str] = None
    cast: List[str]
    rating: Optional[float] = None
    summary: str


# -----------------------------
# Model
# -----------------------------
@st.cache_resource
def get_model():
    return ChatMistralAI(
        model="mistral-small-2603"
    )


model = get_model()


# -----------------------------
# Parser
# -----------------------------
parser = PydanticOutputParser(
    pydantic_object=Movie
)


# -----------------------------
# Prompt
# -----------------------------
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
Extract accurate movie information from the user's query.

Rules:
- Do not invent facts.
- Use null for unknown optional fields.
- Return only the structured Movie output.

{format_instructions}
"""
    ),
    (
        "human",
        "{paragraph}"
    )
])


# -----------------------------
# UI
# -----------------------------
st.title("🎬 Movie Information Extractor")
st.caption("Extract structured movie information using LangChain + Mistral AI")

st.divider()

paragraph = st.text_area(
    "Enter movie information",
    placeholder=(
        "Example: Inception is a 2010 science-fiction film directed "
        "by Christopher Nolan. It stars Leonardo DiCaprio, Joseph Gordon-Levitt "
        "and Ellen Page. The movie has a rating of 8.8."
    ),
    height=180
)

extract_button = st.button(
    "🔍 Extract Movie Information",
    use_container_width=True
)


# -----------------------------
# Processing
# -----------------------------
if extract_button:

    if not paragraph.strip():
        st.warning("Please enter some movie information first.")

    else:
        try:
            with st.spinner("Extracting movie information..."):

                final_prompt = prompt.invoke({
                    "paragraph": paragraph,
                    "format_instructions": parser.get_format_instructions()
                })

                response = model.invoke(final_prompt)

                movie_data = parser.parse(response.content)

            st.success("Movie information extracted successfully!")

            # -----------------------------
            # Movie Header
            # -----------------------------
            st.subheader(f"🎥 {movie_data.title}")

            # -----------------------------
            # Basic Information
            # -----------------------------
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Release Year",
                    movie_data.release_year
                    if movie_data.release_year
                    else "Unknown"
                )

            with col2:
                st.metric(
                    "Rating",
                    movie_data.rating
                    if movie_data.rating
                    else "N/A"
                )

            with col3:
                st.metric(
                    "Genres",
                    len(movie_data.genre)
                )

            st.divider()

            # -----------------------------
            # Movie Details
            # -----------------------------
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### 🎭 Genre")

                if movie_data.genre:
                    for genre in movie_data.genre:
                        st.write(f"• {genre}")
                else:
                    st.write("Unknown")

            with col2:
                st.markdown("### 🎬 Director")
                st.write(movie_data.director or "Unknown")

            st.markdown("### 👥 Cast")

            if movie_data.cast:
                st.write(", ".join(movie_data.cast))
            else:
                st.write("Unknown")

            st.markdown("### 📝 Summary")
            st.write(movie_data.summary)

            # -----------------------------
            # Raw Structured Data
            # -----------------------------
            with st.expander("View Structured JSON"):

                st.json(
                    movie_data.model_dump()
                )

        except Exception as e:

            st.error("Failed to extract movie information.")

            with st.expander("Error details"):
                st.exception(e)