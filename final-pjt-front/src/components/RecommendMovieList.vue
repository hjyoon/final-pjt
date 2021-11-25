<template>
  <div>
    <v-row>
      <RecommendMovieListCard
        v-for="movie in movies"
        :key="movie.id"
        :movie="movie"
      ></RecommendMovieListCard>
    </v-row>
  </div>
</template>

<script>
import { mapState } from "vuex";
import RecommendMovieListCard from "@/components/RecommendMovieListCard.vue";

export default {
  name: "MovieList",
  components: { RecommendMovieListCard },
  data: () => ({
    movies: [],
  }),
  methods: {},
  computed: {
    ...mapState(["isLogin"]),
  },
  created: function () {
    (async () => {
      const token = localStorage.getItem("jwt");
      const URL = `https://www.movie-vol.ga/movies/recommend/`;
      const response = await fetch(URL, {
        method: "GET",
        headers: {
          Authorization: `JWT ${token}`,
        },
      });
      if (response.ok) {
        const data = await response.json();
        this.movies.push(...data);
      } else {
        alert("fail");
      }
    })();
  },
};
</script>

<style></style>
