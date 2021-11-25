<template>
  <v-dialog
    :value="dialog"
    @click:outside="closeDialog"
    @keydown.esc="closeDialog"
    max-width="780"
  >
    <v-card>
      <v-card-title>{{ dialog_movie_data.title }}</v-card-title>
      <v-card-subtitle>{{ dialog_movie_data.release_date }}</v-card-subtitle>
      <v-card-text>{{ dialog_movie_data.overview }}</v-card-text>
      <v-card-text>
        <v-row
          align="center"
          class="mx-0"
          v-if="dialog_movie_data.rating_count > 0"
        >
          <v-rating
            :value="dialog_movie_data.rating_average"
            color="amber"
            size="26"
            dense
            readonly
          ></v-rating>
          <div class="grey--text ms-2">
            {{
              `${dialog_movie_data.rating_average} (${dialog_movie_data.rating_count})`
            }}
          </div>
        </v-row>
        <v-row align="center" class="mx-0" v-else>
          <div class="grey--text ms-2">
            {{ "No Rating" }}
          </div>
        </v-row>
        <v-row align="center" class="mx-0">
          <v-btn icon @click="likeMovie()">
            <v-icon v-if="dialog_movie_data.is_liked">mdi-heart</v-icon>
            <v-icon v-else>mdi-heart-outline</v-icon>
          </v-btn>
          <div class="grey--text ms-2">
            {{ `${dialog_movie_data.likes_count}` }}
          </div>
        </v-row>
        <v-row justify="center" class="mx-auto">
          <iframe
            :src="`https://www.youtube.com/embed/${dialog_movie_data.videos[0].key}`"
            width="100%"
            height="438"
          ></iframe>
        </v-row>
      </v-card-text>
      <v-card-subtitle>
        <p class="text-h6 text--primary">추천 리스트</p>
      </v-card-subtitle>
      <v-card-text>
        <v-row>
          <SimilarMovieListCard
            v-for="movie in similar_movies"
            :key="movie.id"
            :movie="movie"
          ></SimilarMovieListCard>
        </v-row>
      </v-card-text>
      <v-divider></v-divider>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="success" @click="closeDialog">Close</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import SimilarMovieListCard from "@/components/SimilarMovieListCard.vue";
import { mapState, mapActions } from "vuex";

export default {
  name: "MovieDialog",
  components: {
    SimilarMovieListCard,
  },
  data: function () {
    return {};
  },
  methods: {
    likeMovie: function () {
      (async () => {
        const token = localStorage.getItem("jwt");
        const URL = `https://www.movie-vol.ga/movies/${this.dialog_movie_data.id}/like/`;
        const method = this.dialog_movie_data.is_liked ? "DELETE" : "POST";
        console.log(method);
        const response = await fetch(URL, {
          method: method,
          headers: {
            Authorization: `JWT ${token}`,
          },
        });
        if (response.ok) {
          //const data = await response.json();
          //console.log(data);
          this.$router.go();
          //this.openCommentDialog();
          this.dialog_movie_data.is_liked = !this.dialog_movie_data.is_liked;
        }
      })();
    },
    ...mapActions(["closeDialog"]),
  },
  computed: {
    ...mapState(["dialog", "dialog_movie_data", "similar_movies"]),
  },
};
</script>

<style></style>
