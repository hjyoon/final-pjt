<template>
  <v-row dense>
    <CommentListCard
      v-for="comment in comment_list"
      :key="comment.id"
      :comment="comment"
    ></CommentListCard>
  </v-row>
</template>

<script>
import { mapState, mapActions } from "vuex";
import CommentListCard from "@/components/CommentListCard.vue";

export default {
  name: "CommentList",
  components: { CommentListCard },
  data: () => ({}),
  methods: {
    ...mapActions(["closeCommentDialog"]),
  },
  computed: {
    ...mapState(["comment_list"]),
  },
};
</script>

<style></style>
