<template>
  <v-col cols="6" sm="4" md="3" lg="2" xl="1">
    <v-card hover>
      <v-img
        :lazy-src="`https://www.themoviedb.org/t/p/w92/${movie.poster_path}`"
        :src="`https://www.themoviedb.org/t/p/original/${movie.poster_path}`"
      >
        <template v-slot:placeholder>
          <v-row class="fill-height ma-0" align="center" justify="center">
            <v-progress-circular
              indeterminate
              color="grey lighten-5"
            ></v-progress-circular>
          </v-row>
        </template>
      </v-img>
    </v-card>
  </v-col>
</template>

<script>
import { mapState, mapActions } from "vuex";

export default {
  name: "RecommendMovieListCard",
  props: {
    movie: Object,
  },
  data: () => ({}),
  methods: {
    ...mapActions(["openDialog"]),
  },
  computed: {
    ...mapState([]),
  },
};
</script>

<style></style>
