<template>
  <v-dialog
    :value="write_dialog"
    fullscreen
    hide-overlay
    transition="dialog-bottom-transition"
    @keydown.esc="closeWriteDialog"
  >
    <v-card>
      <v-toolbar dark color="primary">
        <v-btn icon dark @click="closeWriteDialog">
          <v-icon>mdi-close</v-icon>
        </v-btn>
        <v-toolbar-title>Writing</v-toolbar-title>
        <v-spacer></v-spacer>
        <v-toolbar-items>
          <v-btn dark text @click="save">Save</v-btn>
        </v-toolbar-items>
      </v-toolbar>
      <v-card-title></v-card-title>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-rating
          v-model="$store.state.tmp_article.rating"
          color="amber"
          size="24"
        ></v-rating>
        <v-spacer></v-spacer>
      </v-card-actions>
      <v-card-text>
        <v-autocomplete
          v-model="$store.state.tmp_article.movie_title"
          :items="movie_list"
          chips
          label="Movie"
          outlined
        ></v-autocomplete>
        <v-textarea
          v-model="$store.state.tmp_article.content"
          counter
          label="Content"
          outlined
        ></v-textarea>
        <v-file-input
          show-size
          counter
          label="Picture"
          accept="image/png, image/jpeg"
          prepend-icon="mdi-camera"
          dense
          outlined
        ></v-file-input>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script>
import { mapState, mapActions } from "vuex";

export default {
  name: "WriteDialog",
  data: function () {
    return {
      movie_list: null,
      movie_to_id: null,
      // movie: null,
      // content: null,
      // rating: null,
      // image: null,
    };
  },
  methods: {
    save: function () {
      if (this.update_mode) {
        (async () => {
          const token = localStorage.getItem("jwt");
          const URL = `https://www.movie-vol.ga/community/${this.tmp_article.id}/`;
          const response = await fetch(URL, {
            method: "PUT",
            headers: {
              "Content-Type": "application/json",
              Authorization: `JWT ${token}`,
            },
            body: JSON.stringify({
              content: this.tmp_article.content,
              movie_title: this.tmp_article.movie_title,
              movie: this.movie_to_id.get(this.tmp_article.movie_title),
              rating: this.tmp_article.rating,
              //image: this.$store.state.image,
            }),
          });
          if (response.ok) {
            //const data = await response.json();
            //this.movie_list = data
            //console.log(data);
            this.$router.go();
          }
          this.setUpdateMode(false);
          this.closeWriteDialog();
          this.changeRoute({ name: "Community" });
        })();
      } else {
        (async () => {
          const token = localStorage.getItem("jwt");
          const URL = "https://www.movie-vol.ga/community/";
          const response = await fetch(URL, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Authorization: `JWT ${token}`,
            },
            body: JSON.stringify({
              content: this.tmp_article.content,
              movie_title: this.tmp_article.movie_title,
              movie: this.movie_to_id.get(this.tmp_article.movie_title),
              rating: this.tmp_article.rating,
              //image: this.$store.state.image,
            }),
          });
          if (response.ok) {
            //const data = await response.json();
            //this.movie_list = data
            console.log(this.movie_to_id.get(this.tmp_article.movie_title));
            this.$router.go();
          }
          this.closeWriteDialog();
          this.changeRoute({ name: "Community" });
        })();
      }
    },
    ...mapActions(["closeWriteDialog", "changeRoute", "setUpdateMode"]),
  },
  computed: {
    ...mapState(["write_dialog", "update_mode", "tmp_article"]),
  },
  created: function () {
    // if (this.update_mode) {
    //   this.movie = this.tmp_article.movie_title;
    //   this.content = this.tmp_article.content;
    //   this.rating = this.tmp_article.rating;
    // }
    (async () => {
      const token = localStorage.getItem("jwt");
      const URL = "https://www.movie-vol.ga/movies/list";
      const response = await fetch(URL, {
        method: "GET",
        headers: {
          Authorization: `JWT ${token}`,
        },
      });
      if (response.ok) {
        const data = await response.json();
        this.movie_list = data.map((v) => v.title);
        this.movie_to_id = new Map(data.map((v) => [v.title, v.id]));
      }
    })();
  },
};
</script>

<style></style>
