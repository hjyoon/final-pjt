<template>
  <div>
    <v-row>
      <MovieListCard
        v-for="movie in movies"
        :key="movie.id"
        :movie="movie"
      ></MovieListCard>
    </v-row>
    <InfiniteLoading @infinite="infiniteHandler" spinner="waveDots">
    </InfiniteLoading>
  </div>
</template>

<script>
import { mapState } from "vuex";
import InfiniteLoading from "vue-infinite-loading";
import MovieListCard from "@/components/MovieListCard.vue";

export default {
  name: "MovieList",
  components: { InfiniteLoading, MovieListCard },
  data: () => ({
    page: 1,
    movies: [],
  }),
  methods: {
    infiniteHandler: function ($state) {
      const EACH_LEN = 20;
      (async (page) => {
        const token = localStorage.getItem("jwt");
        const URL = `https://www.movie-vol.ga/movies/?page=${page}`;
        const response = await fetch(URL, {
          method: "GET",
          headers: {
            Authorization: this.isLogin ? `JWT ${token}` : "",
          },
        });
        if (response.ok) {
          const data = await response.json();
          for (let i = 0; i < data.length; i++) {
            if (data[i].rating_count > 0) {
              data[i].rating_average = data[i].rating_average.toFixed(1);
            }
          }
          this.movies.push(...data);
          this.page += 1;
          $state.loaded();
          if (data.length / EACH_LEN < 1) {
            $state.complete();
          }
        } else {
          alert("fail");
        }
      })(this.page);
    },
  },
  computed: {
    ...mapState(["isLogin"]),
  },
};
</script>

<style></style>
