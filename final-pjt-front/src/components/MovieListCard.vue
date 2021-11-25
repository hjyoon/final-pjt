<template>
  <v-col cols="12" sm="6" md="4" lg="3" xl="2">
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
      <v-card-title>{{ movie.title }}</v-card-title>
      <v-card-subtitle>{{ movie.release_date }}</v-card-subtitle>
      <v-card-text>
        <v-row align="center" class="mx-0" v-if="movie.rating_count > 0">
          <v-rating
            :value="movie.rating_average"
            color="amber"
            dense
            half-increments
            readonly
            size="14"
          ></v-rating>
          <div class="grey--text ms-2">
            {{ `${movie.rating_average} (${movie.rating_count})` }}
          </div>
        </v-row>
        <v-row align="center" class="mx-0" v-else>
          <div class="grey--text ms-2">
            {{ "No Rating" }}
          </div>
        </v-row>
      </v-card-text>
      <v-divider class="mx-4"></v-divider>
      <v-card-actions>
        <v-btn color="deep-purple accent-4" text @click="openDialog(movie.id)"
          >Detail</v-btn
        >

        <v-spacer></v-spacer>

        <v-btn icon @click="likeMovie()">
          <v-icon v-if="movie.is_liked">mdi-heart</v-icon>
          <v-icon v-else>mdi-heart-outline</v-icon>
        </v-btn>

        <v-btn icon>
          <v-icon>mdi-bookmark-outline</v-icon>
        </v-btn>

        <v-btn icon>
          <v-icon>mdi-share-variant-outline</v-icon>
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-col>
</template>

<script>
import { mapState, mapActions } from "vuex";

export default {
  name: "MovieListCard",
  props: {
    movie: Object,
  },
  data: () => ({}),
  methods: {
    likeMovie: function () {
      (async () => {
        const token = localStorage.getItem("jwt");
        const URL = `https://www.movie-vol.ga/movies/${this.movie.id}/like/`;
        const method = this.movie.is_liked ? "DELETE" : "POST";
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
          this.movie.is_liked = !this.movie.is_liked;
        }
      })();
    },
    ...mapActions(["openDialog"]),
  },
  computed: {
    ...mapState([]),
  },
};
</script>

<style></style>
