<template>
  <v-dialog
    :value="comment_dialog"
    fullscreen
    hide-overlay
    transition="dialog-bottom-transition"
    @keydown.esc="closeCommentDialog"
  >
    <v-card>
      <v-toolbar dark color="primary">
        <v-btn icon dark @click="closeCommentDialog">
          <v-icon>mdi-close</v-icon>
        </v-btn>
        <v-toolbar-title>Comment</v-toolbar-title>
      </v-toolbar>
      <CommentList></CommentList>
    </v-card>
  </v-dialog>
</template>

<script>
import { mapState, mapActions } from "vuex";
import CommentList from "@/components/CommentList.vue";

export default {
  name: "CommentDialog",
  components: { CommentList },
  data: function () {
    return {};
  },
  methods: {
    ...mapActions(["closeCommentDialog"]),
  },
  computed: {
    ...mapState(["comment_dialog"]),
  },
};
</script>

<style></style>
