<template>
  <v-container>
    <MovieList></MovieList>
    <MovieDialog></MovieDialog>
  </v-container>
</template>

<script>
import MovieList from "@/components/MovieList.vue";
import MovieDialog from "@/components/MovieDialog.vue";
import { mapActions } from "vuex";

export default {
  name: "Home",
  components: { MovieList, MovieDialog },
  methods: {
    ...mapActions(["setAppTitle", "setSelectedMenu"]),
  },
  created: function () {
    this.setAppTitle("Home");
    this.setSelectedMenu(0);
  },
};
</script>
