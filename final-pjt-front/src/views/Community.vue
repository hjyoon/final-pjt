<template>
  <v-container>
    <div v-if="isLogin">
      <v-btn color="pink" fab dark fixed bottom right @click="openWriteDialog">
        <v-icon>mdi-pencil-plus</v-icon>
      </v-btn>
      <ArticleList></ArticleList>
      <WriteDialog></WriteDialog>
      <CommentDialog></CommentDialog>
    </div>
    <p class="text-justify" v-else>로그인을 먼저 해주세요.</p>
  </v-container>
</template>

<script>
import { mapState, mapActions } from "vuex";
import ArticleList from "@/components/ArticleList.vue";
import WriteDialog from "@/components/WriteDialog.vue";
import CommentDialog from "@/components/CommentDialog.vue";

export default {
  name: "Community",
  components: { WriteDialog, ArticleList, CommentDialog },
  methods: {
    ...mapActions(["setAppTitle", "setSelectedMenu", "openWriteDialog"]),
  },
  computed: {
    ...mapState(["isLogin"]),
  },
  created: function () {
    this.setAppTitle("Community");
    this.setSelectedMenu(2);
  },
};
</script>
